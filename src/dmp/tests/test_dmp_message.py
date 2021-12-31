#!/usr/bin/env python3
import unittest

from dmp.dmp_message import (
    parse_message,
    DmpDeviceStatusMessage,
    DmpArmingStatusMessage,
    DmpSystemMessageMessage,
    DmpLowBatteryMessage,
)
from dmp.dmp_types import DmpEventType


class TestDmpMessage(unittest.TestCase):
    def testDoorOpen(self):
        msg = parse_message('\x02E60F   1294 &    0Zc\\020\\t "DO\\z 501\\')

        assert isinstance(
            msg, DmpDeviceStatusMessage
        ), "Expecting a DmpDeviceStatusMessage"
        self.assertEqual(msg.zone.number, "501")
        self.assertIsNone(msg.zone.name, "No name specified in message")
        self.assertEqual(msg.event_type, DmpEventType.DOOR_STATUS_OPEN)

    def testDoorClosed(self):
        msg = parse_message('\x02E65A   1294 &    0Zc\\020\\t "DC\\z 501\\')

        assert isinstance(
            msg, DmpDeviceStatusMessage
        ), "Expecting a DmpDeviceStatusMessage"
        self.assertEqual(msg.zone.number, "501")
        self.assertIsNone(msg.zone.name, "No name specified in message")
        self.assertEqual(msg.event_type, DmpEventType.DOOR_STATUS_CLOSED)

    def testDisarm(self):
        msg = parse_message(
            '\x02159C   1294 &    1Zq\\062\\t "OP\\u 00107"JEFF FOB        \\a 001"PERIMETER       \\'
        )

        assert isinstance(
            msg, DmpArmingStatusMessage
        ), "Expecting a DmpArmingStatusMessage"

        self.assertEqual(msg.area.number, "001")
        self.assertEqual(msg.area.name, "PERIMETER")
        self.assertEqual(msg.event_type, DmpEventType.AREA_DISARMED)

    def testArm(self):
        msg = parse_message(
            '\x027E0E   1294 &    0Zq\\062\\t "CL\\u 00000"NO CODE REQUIRED\\a 002"INTERIOR        \\'
        )

        assert isinstance(
            msg, DmpArmingStatusMessage
        ), "Expecting a DmpArmingStatusMessage"
        self.assertEqual(msg.area.number, "002")
        self.assertEqual(msg.area.name, "INTERIOR")
        self.assertEqual(msg.event_type, DmpEventType.AREA_ARMED)

    def testLowBattery(self):
        msg = parse_message(
            '\x026565   1294 &    0Zd\\060\\t "A1\\z 630"REPEATER LAUNDRY\\a 001"PERIMETER       \\'
        )

        assert isinstance(msg, DmpLowBatteryMessage), "Expecting a DmpLowBatteryMessage"
        self.assertEqual(msg.zone.number, "630")
        self.assertEqual(msg.zone.name, "REPEATER LAUNDRY")
        self.assertEqual(msg.area.number, "001")
        self.assertEqual(msg.area.name, "PERIMETER")
        self.assertEqual(msg.event_type, DmpEventType.ZONE_AUXILIARY_1)

    def testSystemMessage(self):
        msg = parse_message("\x0227F7   1294 &    0Zs\\014\\t 071\\")

        assert isinstance(
            msg, DmpSystemMessageMessage
        ), "Expecting a DmpSystemMessageMessage"
        self.assertEqual(msg.event_type, DmpEventType.SYSTEM_TIME_REQUEST)


if __name__ == "__main__":
    unittest.main()
