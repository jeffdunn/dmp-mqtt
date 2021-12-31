#!/usr/bin/env python3
import argparse
import asyncio
import logging

from dmp.bridge import run_dmp_mqtt_bridge


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("gmqtt").setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        description="Bridge between DMP security system and MQTT broker"
    )
    parser.add_argument(
        "--listen-port",
        type=int,
        help="Port to listen on for messages from MQTT, configured via the NET route",
        required=True,
    )
    parser.add_argument(
        "--dmp-server-host",
        type=str,
        help="Host for the DMP security system",
        required=True,
    )
    parser.add_argument(
        "--dmp-server-port",
        type=int,
        help="Port for sending commands to the DMP security system",
        required=True,
    )
    parser.add_argument(
        "--dmp-account-number", type=str, help="DMP account number", required=True
    )
    parser.add_argument(
        "--dmp-remote-key", type=str, help="DMP remote key", required=True
    )
    parser.add_argument(
        "--mqtt-broker-host", type=str, help="Host for the MQTT broker", required=True
    )
    parser.add_argument(
        "--mqtt-username",
        type=str,
        help="Username for connecting to the MQTT broker",
        required=True,
    )
    parser.add_argument(
        "--mqtt-password",
        type=str,
        help="Password for connecting to the MQTT broker",
        required=True,
    )
    args = parser.parse_args()

    await run_dmp_mqtt_bridge(
        listen_port=args.listen_port,
        dmp_server_host=args.dmp_server_host,
        dmp_server_port=args.dmp_server_port,
        dmp_account_number=args.dmp_account_number,
        dmp_remote_key=args.dmp_remote_key,
        mqtt_broker_host=args.mqtt_broker_host,
        mqtt_username=args.mqtt_username,
        mqtt_password=args.mqtt_password,
    )


if __name__ == "__main__":
    asyncio.run(main())
