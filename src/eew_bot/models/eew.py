from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Warnarea:
    chiiki: List[str]
    Shindo1: List[str]
    Arrive: List[bool]


@dataclass
class EEW:
    report_no: int
    title: str
    report_time: str

    hypo_name: str
    magnitude: float
    depth: int
    max_shindo: Optional[str]

    warn_area: List[str]

    is_sea: bool
    is_test: bool
    is_plum: bool
    is_warn: bool
    is_final: bool
    is_cancel: bool
