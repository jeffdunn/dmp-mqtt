#!/usr/bin/env python3
import re
from dataclasses import dataclass
from typing import Optional, Tuple

from dmp.exceptions import DmpInvalidMessageException


@dataclass(frozen=True)
class DmpZone:
    number: str
    name: Optional[str] = None


@dataclass(frozen=True)
class DmpArea:
    number: str
    name: str


@dataclass(frozen=True)
class DmpDevice:
    number: str
    name: Optional[str] = None


def dmp_section(regex: str, construct):
    def decorator(cls):
        cls._regex = regex
        cls._construct = construct
        return cls

    return decorator


@dmp_section(
    regex=r'z (?P<number>[ \d]{1,3})(?P<name>".*?)?\\',
    construct=lambda cls, match: cls(
        zone=DmpZone(
            number=match.group("number").strip(),
            name=match.group("name")[1:].strip() if match.group("name") else None,
        )
    ),
)
@dataclass(frozen=True)
class _DmpZoneSection:
    zone: DmpZone


@dmp_section(
    regex=r'z (?P<number>[ \d]{1,3})(?P<name>".*?)?\\',
    construct=lambda cls, match: cls(
        zone=DmpZone(
            number=match.group("number").strip(),
            name=match.group("name")[1:].strip() if match.group("name") else None,
        )
    ),
)
@dataclass(frozen=True)
class _DmpOptionalZoneSection:
    zone: Optional[DmpZone] = None


@dmp_section(
    regex=r'a (?P<number>[ \d]{1,3})"(?P<name>.*?)\\',
    construct=lambda cls, match: cls(
        area=DmpArea(
            number=match.group("number").strip(),
            name=match.group("name").strip(),
        )
    ),
)
@dataclass(frozen=True)
class _DmpAreaSection:
    area: DmpArea


@dmp_section(
    regex=r'a (?P<number>[ \d]{1,3})"(?P<name>.*?)\\',
    construct=lambda cls, match: cls(
        area=DmpArea(
            number=match.group("number").strip(),
            name=match.group("name").strip(),
        )
    ),
)
@dataclass(frozen=True)
class _DmpAreaOptionalSection:
    area: Optional[DmpArea] = None


@dmp_section(
    regex=r'v (?P<number>[ \d]{1,3})(?P<name>".*?)?\\',
    construct=lambda cls, match: cls(
        device=DmpDevice(
            number=match.group("number").strip(),
            name=match.group("name")[1:].strip() if match.group("name") else None,
        )
    ),
)
@dataclass(frozen=True)
class _DmpDeviceSection:
    device: Optional[DmpDevice] = None


@dmp_section(
    regex=r"g (?P<number>[ \d]{1,6})\\",
    construct=lambda cls, match: cls(equipment_id=match.group("number").strip()),
)
@dataclass(frozen=True)
class _DmpServiceCodeSection:
    equipment_id: str


@dmp_section(
    regex=r"m[ YN](?P<number>\d{5})\\",
    construct=lambda cls, match: cls(service_code=match.group("number").strip()),
)
@dataclass(frozen=True)
class _DmpProgrammingSection:
    service_code: Optional[str] = None
