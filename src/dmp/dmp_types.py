#!/usr/bin/env python3

from enum import Enum


class DocEnum(Enum):
    def __new__(cls, value, doc=None):
        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self


class DmpEventType(DocEnum):
    # Zones
    ZONE_BLANK = "BL", "Blank"
    ZONE_FIRE = "FI", "Fire"
    ZONE_BURGLARY = "BU", "Burglary"
    ZONE_SUPERVISORY = "SV", "Supervisory"
    ZONE_PANIC = "PN", "Panic"
    ZONE_EMERGENCY = "EM", "Emergency"
    ZONE_AUXILIARY_1 = "A1", "Auxiliary 1"
    ZONE_AUXILIARY_2 = "A2", "Auxiliary 2"
    # Access
    ACCESS_DOOR_ACCESS_GRANTED = "DA", "Door Access Granted"
    ACCESS_DOOR_ACCESS_DENIED_ARMED_AREA = "AA", "Door Access Denied: Armed Area"
    ACCESS_DOOR_ACCESS_DENIED_INVALID_AREA = "IA", "Door Access Denied: Invalid Area"
    ACCESS_DOOR_ACCESS_DENIED_INVALID_TIME = "IT", "Door Access Denied: Invalid Time"
    ACCESS_DOOR_ACCESS_DENIED_PREVIOUS_ACCESS = (
        "AP",
        "Door Access Denied: Previous Access",
    )
    ACCESS_DOOR_ACCESS_DENIED_INVALID_CODE = "IC", "Door Access Denied: Invalid Code"
    ACCESS_DOOR_ACCESS_DENIED_INVALID_LEVEL = "IL", "Door Access Denied: Invalid Level"
    # Status
    DOOR_STATUS_OPEN = "DO", "Door Status: Open"
    DOOR_STATUS_CLOSED = "DC", "Door Status: Closed"
    DOOR_STATUS_HELD_OPEN = "HO", "Door Status: Held Open"
    DOOR_STATUS_FORCED_OPEN = "FO", "Door Status: Forced Open"
    OUTPUT_STATUS_ON = "ON", "Output Status: On"
    OUTPUT_STATUS_OFF = "OF", "Output Status: Off"
    OUTPUT_STATUS_PULSE = "PL", "Output Status: Pulse"
    OUTPUT_STATUS_TEMPORAL = "TP", "Output Status: Temporal"
    # Equipment
    EQUIPMENT_REPAIR = "RP", "Equipment: Repair"
    EQUIPMENT_REPLACE = "RL", "Equipment: Replace"
    EQUIPMENT_ADD = "AD", "Equipment: Add"
    EQUIPMENT_REMOVE = "RM", "Equipment: Remove"
    EQUIPMENT_ADJUST = "AJ", "Equipment: Adjust"
    EQUIPMENT_TEST = "TS", "Equipment: Test"
    # Qualifier
    SERVICE = "DT", "Service"
    ALL_AREAS_ARMED = "AC", "All Areas Armed"
    # Arming
    AREA_DISARMED = "OP", "Area Disarmed"
    AREA_ARMED = "CL", "Area Armed"
    AREA_LATE_TO_ARM = "LA", "Area Late to Arm"
    # Schedule
    PERMANENT_SCHEDULE = "PE", "Permanent Schedule"
    TEMPORARY_SCHEDULE = "TE", "Temporary Schedule"
    PRIMARY_SCHEDULE = "PR", "Primary Schedule"
    SECONDARY_SCHEDULE = "SE", "Secondary Schedule"
    SCHEDULE_SHIFT_1 = "S1", "Shift 1"
    SCHEDULE_SHIFT_2 = "S2", "Shift 2"
    SCHEDULE_SHIFT_3 = "S3", "Shift 3"
    SCHEDULE_SHIFT_4 = "S4", "Shift 4"
    # System Messages
    SYSTEM_AC_POWER_RESTORED = "000", "AC Power Restored"
    SYSTEM_STANDBY_BATTERY_RESTORED = "001", "Standby Battery Restored"
    SYSTEM_COMMUNICATIONS_LINE_RESTORED = "002", "Communications Line Restored"
    SYSTEM_PANEL_TAMPER_RESTORED = "003", "Panel Tamper Restored"
    SYSTEM_BACKUP_COMMUNICATIONS_RESTORED = "004", "Backup Communications Restored"
    SYSTEM_PANEL_GROUND_RESTORED = "005", "Panel Ground Restored"
    SYSTEM_SYSTEM_NOT_ARMED_BY_SCHEDULED_TIME = (
        "006",
        "System Not Armed by Scheduled Time",
    )
    SYSTEM_AUTOMATIC_COMMUNICATION_TEST = "007", "Automatic Communication Test"
    SYSTEM_AC_POWER_FAILURE = "008", "AC Power Failure"
    SYSTEM_LOW_STANDBY_BATTERY = "009", "Low Standby Battery"
    SYSTEM_LOW_COMMUNICATIONS_SIGNAL = "010", "Low Communications Signal"
    SYSTEM_PANEL_TAMPER = "011", "Panel Tamper"
    SYSTEM_BACKUP_COMMUNICATIONS_FAILURE = "012", "Backup Communications Failure"
    SYSTEM_PANEL_GROUND_FAULT = "013", "Panel Ground Fault"
    SYSTEM_NON_ALARM_MESSAGE_OVERFLOW = "014", "Non-Alarm Message Overflow"
    SYSTEM_AMBUSH_SILENT_ALARM = "015", "Ambush/Silent Alarm"
    SYSTEM_ALARM_MESSAGE_OVERFLOW = "018", "Alarm Message Overflow"
    SYSTEM_LOCAL_PANEL_TEST = "023", "Local Panel test"
    SYSTEM_AUXILIARY_FUSE_TROUBLE = "026", "Auxiliary fuse Trouble"
    SYSTEM_AUXILIARY_FUSE_RESTORED = "027", "Auxiliary Fuse Restored"
    SYSTEM_TELEPHONE_LINE_1_FAULT = "028", "Telephone line 1 Fault"
    SYSTEM_TELEPHONE_LINE_1_RESTORE = "029", "Telephone line 1 Restore"
    SYSTEM_TELEPHONE_LINE_2_FAULT = "030", "Telephone line 2 Fault"
    SYSTEM_TELEPHONE_LINE_2_RESTORE = "031", "Telephone line 2 Restore"
    SYSTEM_SUPERVISED_WIRELESS_INTERFERENCE = "032", "Supervised wireless Interference"
    SYSTEM_EARLY_MORNING_AMBUSH = "033", "Early Morning Ambush"
    SYSTEM_ALARM_SILENCED = "034", "Alarm Silenced"
    SYSTEM_ALARM_BELL_NORMAL = (
        "035",
        "Alarm Bell Normal",
    )  # not implemented per dmp docs
    SYSTEM_BELL_CIRCUIT_TROUBLE = "038", "Bell Circuit Trouble"
    SYSTEM_BELL_CIRCUIT_RESTORED = "039", "Bell Circuit Restored"
    SYSTEM_FIRE_ALARM_MESSAGE_OVERFLOW = "040", "Fire Alarm Message Overflow"
    SYSTEM_PANIC_ZONE_ALARM_OVERFLOW = "041", "Panic Zone Alarm Overflow"
    SYSTEM_BURGLARY_ZONE_ALARM_OVERFLOW = "042", "Burglary Zone Alarm Overflow"
    SYSTEM_BELL_FUSE_TROUBLE = "043", "Bell Fuse Trouble"
    SYSTEM_FIRE_BURGLARY_TROUBLE_OVERFLOW = "044", "Fire/Burglary Trouble Overflow"
    SYSTEM_ABORT_SIGNAL_RECEIVED = "045", "Abort Signal Received"
    SYSTEM_ZONE_SWINGER_AUTOMATICALLY_BYPASSED = (
        "046",
        "Zone Swinger Automatically Bypassed",
    )
    SYSTEM_ZONE_SWINGER_AUTOMATICALLY_RESET = "047", "Zone Swinger Automatically Reset"
    SYSTEM_BACKUP_BATTERY_CRITICAL_LAST_MESSAGE_BEFORE_POWEROFF = (
        "048",
        "Backup Battery Critical - Last Message Before Poweroff",
    )
    SYSTEM_CANCEL_SIGNAL_RECEIVED = "049", "Cancel Signal Received"
    SYSTEM_SUPERVISED_WIRELESS_TROUBLE = "050", "Supervised Wireless Trouble"
    SYSTEM_REMOTE_PROGRAMMING = "051", "Remote Programming"
    SYSTEM_BELL_FUSE_RESTORED = "053", "Bell Fuse Restored"
    SYSTEM_UNSUCCESSFUL_REMOTE_CONNECT = "054", "Unsuccessful Remote connect"
    SYSTEM_TIME_REQUEST = "071", "Time Request"
    SYSTEM_NETWORK_TROUBLE = "072", "Network trouble"
    SYSTEM_NETWORK_RESTORAL = "073", "Network Restoral"
    SYSTEM_PANEL_TAMPER_DURING_ARMED_STATE = "074", "Panel Tamper during Armed State"
    SYSTEM_UNAUTHORIZED_ENTRY = "077", "Unauthorized Entry"
    SYSTEM_SYSTEM_RECENTLY_ARMED = "078", "System Recently Armed"
    SYSTEM_SIGNAL_DURING_OPENED_PERIOD = "079", "Signal During Opened Period"
    SYSTEM_EXIT_ERROR = "080", "Exit Error"
    SYSTEM_REMOTE_PROGRAMMING_COMPLETE = "083", "Remote Programming Complete"
    SYSTEM_REMOTE_COMMAND_RECEIVED = "084", "Remote Command Received"
    SYSTEM_LOCAL_PROGRAMMING = "086", "Local programming"
    SYSTEM_TRANSMIT_FAILED_MESSAGES_NOT_SENT = (
        "087",
        "Transmit failed - Messages Not Sent",
    )
    SYSTEM_AUTOMATIC_TEST_TROUBLED_SYSTEM = "088", "Automatic Test - Troubled system"
    SYSTEM_SUPERVISED_WIRELESS_RESTORED = "089", "Supervised Wireless Restored"
    SYSTEM_SERVICES_REQUESTED = "091", "Services Requested"
    SYSTEM_NO_ARM_DISARM_ACTIVITY = "092", "No Arm/Disarm Activity"
    SYSTEM_USER_ACTIVITY_NOT_DETECTED = "093", "User activity Not detected"
    SYSTEM_ACTIVITY_CHECK_ENABLED = "094", "Activity Check Enabled"
    SYSTEM_ACTIVITY_CHECK_DISABLED = "095", "Activity Check disabled"
    SYSTEM_ALARM_VERIFIED = "096", "Alarm Verified"
    SYSTEM_NETWORK_TEST_OK = "097", "Network Test OK"
    SYSTEM_DEVICE_MISSING = "101", "Device Missing"
    SYSTEM_DEVICE_RESTORED = "102", "Device Restored"
    SYSTEM_EXCESSIVE_CELLULAR_COMMUNICATION = "121", "Excessive Cellular communication"
    SYSTEM_CELL_COMMUNICATION_SUPPRESSED_EXCESSIVE_DATA = (
        "122",
        "Cell Communication Suppressed: Excessive data",
    )
    # more for cell systems, i'm lazy
    # Holidays
    HOLIDAY_SCHEDULE_A = "HA", "Holiday Schedule A"
    HOLIDAY_SCHEDULE_B = "HB", "Holiday Schedule B"
    HOLIDAY_SCHEDULE_C = "HC", "Holiday Schedule C"
    # User Code
    USER_CODE_ADDED = "AD", "User Code Added"
    USER_CODE_CHANGED = "CH", "User Code Changed"
    USER_CODE_DELETED = "DE", "User Code Deleted"
    # Service User
    START_SERVICE_USER = "ST", "Start Service User"
    STOP_SERVICE_USER = "SP", "Stop Service User"


_members = {member.value: member for member in DmpEventType.__members__.values()}


def parse_event_type(event_type: str) -> DmpEventType:
    return _members[event_type.lstrip('"')]
