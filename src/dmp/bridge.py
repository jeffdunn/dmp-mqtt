#!/usr/bin/env python3
import asyncio
import logging
from typing import AsyncGenerator

from gmqtt import Client as MQTTClient

from dmp.dmp_message import (
    DmpArmingStatusMessage,
    DmpDeviceStatusMessage,
    DmpLowBatteryMessage,
    DmpMessage,
    DmpZoneAlarmMessage,
    parse_message as dmp_parse_message,
)
from dmp.dmp_types import DmpEventType
from dmp.exceptions import DmpInvalidMessageException


async def run_dmp_mqtt_bridge(
    listen_port: int,
    dmp_server_host: str,
    dmp_server_port: int,
    dmp_account_number: str,
    dmp_remote_key: str,
    mqtt_broker_host: str,
    mqtt_username: str,
    mqtt_password: str,
) -> None:
    dmp_writer = DmpMessageWriter(
        dmp_server_host=dmp_server_host,
        dmp_server_port=dmp_server_port,
        dmp_account_number=dmp_account_number,
        dmp_remote_key=dmp_remote_key,
    )

    command_topic = f"dmp/{dmp_account_number}/alarm/set"

    mqtt_client = MQTTClient("dmp-mqtt")
    mqtt_client.set_auth_credentials(mqtt_username, mqtt_password)

    async def on_mqtt_message_received(client, topic, payload, qos, properties) -> int:
        assert topic == command_topic
        if payload == b"ARM_HOME":
            await dmp_writer.arm_home()
        elif payload == b"ARM_AWAY":
            await dmp_writer.arm_away()
        else:
            logging.warning(f"Unknown command payload: {payload.decode('utf-8')}")
        return 0

    mqtt_client.on_message = on_mqtt_message_received

    logging.info(f"Connecting to MQTT server: {mqtt_broker_host}")
    await mqtt_client.connect(mqtt_broker_host)
    mqtt_client.subscribe(command_topic)

    listener = DmpMessageListener(
        listen_port=listen_port,
        dmp_server_host=dmp_server_host,
        dmp_account_number=dmp_account_number,
    )
    await translate_dmp_to_mqtt(listener, mqtt_client, dmp_account_number)


async def translate_dmp_to_mqtt(
    listener: "DmpMessageListener",
    mqtt_client: MQTTClient,
    dmp_account_number: str,
) -> None:
    def publish(topic: str, payload: str, **kwargs) -> None:
        logging.debug(f"Publishing to MQTT: {topic} --> {payload}")
        mqtt_client.publish(topic, payload, **kwargs)

    async for message in listener.listen():
        if isinstance(message, DmpZoneAlarmMessage):
            publish(
                f"dmp/{dmp_account_number}/alarm",
                "triggered",
                retain=True,
            )
        elif isinstance(message, DmpLowBatteryMessage):
            publish(
                f"dmp/{dmp_account_number}/low_battery",
                message.zone.name or message.zone.number,
            )
        elif isinstance(message, DmpArmingStatusMessage):
            if message.event_type == DmpEventType.AREA_DISARMED:
                status = "disarmed"
            elif message.event_type == DmpEventType.AREA_ARMED:
                status = "armed_home" if message.area.number == "001" else "armed_away"
            else:
                logging.warning(f"Unknown arming status message: {message}")
                continue
            publish(
                f"dmp/{dmp_account_number}/alarm",
                status,
                retain=True,
            )
        elif isinstance(message, DmpDeviceStatusMessage):
            on_events = {
                DmpEventType.DOOR_STATUS_OPEN,
                DmpEventType.DOOR_STATUS_HELD_OPEN,
                DmpEventType.DOOR_STATUS_FORCED_OPEN,
                DmpEventType.OUTPUT_STATUS_ON,
                DmpEventType.OUTPUT_STATUS_PULSE,
                DmpEventType.OUTPUT_STATUS_TEMPORAL,
            }
            zone = message.zone
            if zone:
                publish(
                    f"dmp/{dmp_account_number}/status/{zone.number}",
                    "on" if message.event_type in on_events else "off",
                    retain=True,
                )


class DmpMessageListener:
    def __init__(
        self,
        listen_port: int,
        dmp_server_host: str,
        dmp_account_number: str,
    ) -> None:
        self._listen_port = listen_port
        self._dmp_server_host = dmp_server_host
        self._dmp_account_number = dmp_account_number
        self._queue: asyncio.Queue[DmpMessage] = asyncio.Queue()

    async def listen(self) -> AsyncGenerator[DmpMessage, None]:
        logging.info(f"Starting server on port {self._listen_port}")
        await asyncio.start_server(self._on_connect, "0.0.0.0", self._listen_port)
        logging.info(f"Listening for incoming DMP message on port {self._listen_port}")

        while True:
            yield (await self._queue.get())

    async def _on_connect(self, reader, writer) -> None:
        peer = writer.get_extra_info("peername")
        logging.debug(f"Connection from {peer} on {self._listen_port}")

        while True:
            try:
                data = (await reader.readuntil(b"\r")).decode("utf-8")
                if not data:
                    return
            except asyncio.IncompleteReadError:
                logging.debug(f"{peer} disconnected")
                return

            logging.debug(f"Received raw message from DMP: {repr(data)}")
            try:
                message = dmp_parse_message(data.rstrip())
                if message:
                    logging.debug(f"Parsed DMP message: {message}")
                    await self._queue.put(message)
            except DmpInvalidMessageException:
                logging.warning(f"Invalid DMP message: {message}")

            writer.write(f"\x02{self._dmp_account_number.rjust(5)}\x06\x0D".encode())
            await writer.drain()


class DmpMessageWriter:
    def __init__(
        self,
        dmp_server_host: str,
        dmp_server_port: int,
        dmp_account_number: str,
        dmp_remote_key: str,
    ) -> None:
        self._dmp_server_host = dmp_server_host
        self._dmp_server_port = dmp_server_port
        self._dmp_account_number = dmp_account_number
        self._dmp_remote_key = dmp_remote_key

    async def arm_away(self) -> None:
        logging.info("Arming alarm in 'away' mode")
        await self._send("!C01,YN")
        await self._send("!C02,YN")

    async def arm_home(self) -> None:
        logging.info("Arming alarm in 'home' mode")
        await self._send("!C01,YN")

    async def _send(self, msg: str) -> bytes:
        reader, writer = await asyncio.open_connection(
            self._dmp_server_host, self._dmp_server_port
        )

        account_number_padded = self._dmp_account_number.rjust(5)

        writer.write(f"@{account_number_padded}!V0\r".encode())
        await writer.drain()
        await asyncio.sleep(2)

        writer.write(
            f"@{account_number_padded}!V2{self._dmp_remote_key.ljust(16)}\r".encode()
        )
        await writer.drain()
        await asyncio.sleep(0.2)

        writer.write(f"@{account_number_padded}{msg}\r".encode())
        await writer.drain()
        await asyncio.sleep(0.2)

        writer.write("@{account_number_padded}!V0\r".encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        resp = await reader.read(256)
        logging.debug(f"Received response to command: {resp.decode('utf-8', 'ignore')}")
        return resp
