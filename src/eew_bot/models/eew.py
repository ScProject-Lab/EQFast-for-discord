from dataclasses import dataclass


@dataclass
class Warnarea:
    chiiki: list[str]
    Shindo1: list[str]
    Arrive: list[bool]


@dataclass
class EEW:
    type: str
    Title: str
    EventID: str
    Serial: int
    AnnouncedTime: str
    Hypocenter: str
    Magunitude: float
    Depth: int
    MaxIntensity: str
    Warnarea: list[Warnarea]
    isSea: bool
    isTraining: bool
    isAssumption: bool
    isWarn: bool
    isFinal: bool
    isCancel: bool
