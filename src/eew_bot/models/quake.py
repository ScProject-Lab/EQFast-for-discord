from dataclasses import dataclass


@dataclass
class Hypocenter:
    depth: int
    magnitude: float
    name: str
    maxScale: int


@dataclass
class Earthquake:
    domestic_tsunami: str
    foreign_tsunami: str
    hypocenter: Hypocenter
    max_scale: int
    time: str


@dataclass
class Issue:
    source: str
    correct: str
    type: str


@dataclass
class Point:
    addr: str
    is_area: bool
    pref: str
    scale: int


@dataclass
class EarthquakeEvent:
    id: str
    code: int
    issue: Issue
    earthquake: Earthquake
    points: "list[Point]"


events: "list[EarthquakeEvent]"
