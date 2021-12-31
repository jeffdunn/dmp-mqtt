#!/usr/bin/env python3
import dataclasses
import logging
import re
from typing import Optional

from dmp.dmp_section import (
    DmpArea,
    DmpDevice,
    DmpZone,
    _DmpAreaOptionalSection,
    _DmpAreaSection,
    _DmpDeviceSection,
    _DmpOptionalZoneSection,
    _DmpProgrammingSection,
    _DmpServiceCodeSection,
    _DmpZoneSection,
)
from dmp.dmp_types import DmpEventType, parse_event_type
from dmp.exceptions import DmpInvalidMessageException


HEADER_REGEX = re.compile(
    r"^\x02(?P<crc>.{4})"
    r"  "
    r"(?P<account_number>[ \d]{5})"
    r" &"
    r"(?P<minutes_ago>[ \d]{5})"
    r"Z(?P<event_key>[a-z])\\"
    r"(?P<message_length>\d{3})"
    r'\\t (?P<event_type>"[A-Z][A-Z0-9]|\d{3})\\'
)


def parse_message(data: str) -> Optional["DmpMessage"]:
    """
    See https://buy.dmp.com/dmp/products/documents/LT-1035.pdf for spec.
    """

    match = HEADER_REGEX.match(data)
    if not match:
        raise DmpInvalidMessageException(data)

    cls = _events.get(match.group("event_key"))
    if not cls:
        return None

    return cls._parse(
        data[len(match.group(0)) :],
        crc=match.group("crc"),
        account_number=match.group("account_number").lstrip(),
        minutes_ago=int(match.group("minutes_ago").lstrip()),
        event_type=parse_event_type(match.group("event_type")),
    )


_events = {}


def dmp_event_character(char: str):
    def decorator(cls):
        _events[char] = cls
        return cls

    return decorator


def _get_section_regex(section_cls) -> str:
    if not hasattr(section_cls, "_regex"):
        raise Exception("Class is not annotated with @dmp_section")

    return str(section_cls._regex)


@dataclasses.dataclass(frozen=True)
class DmpMessage:
    crc: str
    account_number: str
    minutes_ago: int
    event_type: DmpEventType

    @classmethod
    def _parse(cls, data: str, **kwargs):
        mapping = {
            _get_section_regex(base)[0]: base
            for base in cls.__bases__
            if base is not DmpMessage
        }

        remaining_data = data
        while remaining_data:
            key = remaining_data[0]
            section_cls = mapping.get(key)
            if not section_cls:
                section, remaining_data = remaining_data.split("\\", 1)
                logging.warning(f"Unknown message subsection: {section}\\")
                continue

            match = re.match(_get_section_regex(section_cls), remaining_data)
            if not match:
                raise DmpInvalidMessageException(data)

            remaining_data = remaining_data[len(match.group(0)) :]
            construct = section_cls._construct  # type: ignore
            kwargs.update(construct(section_cls, match).__dict__)
        return cls(**kwargs)


@dmp_event_character("a")
@dataclasses.dataclass(frozen=True)
class DmpZoneAlarmMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("b")
@dataclasses.dataclass(frozen=True)
class DmpZoneForceMessage(_DmpZoneSection, _DmpAreaSection, DmpMessage):
    pass


@dmp_event_character("d")
@dataclasses.dataclass(frozen=True)
class DmpLowBatteryMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("f")
@dataclasses.dataclass(frozen=True)
class DmpZoneFailMessage(_DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("h")
@dataclasses.dataclass(frozen=True)
class DmpZoneMissingMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("k")
@dataclasses.dataclass(frozen=True)
class DmpZoneVerifyMessage(_DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("r")
@dataclasses.dataclass(frozen=True)
class DmpZoneRestoreMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("t")
@dataclasses.dataclass(frozen=True)
class DmpZoneTroubleMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("w")
@dataclasses.dataclass(frozen=True)
class DmpZoneFaultMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("x")
@dataclasses.dataclass(frozen=True)
class DmpZoneBypassMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("y")
@dataclasses.dataclass(frozen=True)
class DmpZoneResetMessage(_DmpAreaOptionalSection, _DmpZoneSection, DmpMessage):
    pass


@dmp_event_character("j")
@dataclasses.dataclass(frozen=True)
class DmpDoorAccessMessage(_DmpDeviceSection, DmpMessage):
    pass


# Schedules not implemented


@dmp_event_character("q")
@dataclasses.dataclass(frozen=True)
class DmpArmingStatusMessage(_DmpAreaSection, DmpMessage):
    pass


# User codes not implemented
# Holidays not implemented
# Equipment not implemented


@dmp_event_character("m")
@dataclasses.dataclass(frozen=True)
class DmpServiceCodeMessage(_DmpServiceCodeSection, DmpMessage):
    pass


@dmp_event_character("s")
@dataclasses.dataclass(frozen=True)
class DmpSystemMessageMessage(_DmpProgrammingSection, DmpMessage):
    pass


@dmp_event_character("c")
@dataclasses.dataclass(frozen=True)
class DmpDeviceStatusMessage(_DmpDeviceSection, _DmpOptionalZoneSection, DmpMessage):
    pass
