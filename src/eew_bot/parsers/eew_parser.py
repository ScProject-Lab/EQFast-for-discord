from typing import Optional
from eew_bot.models.eew import EEW


def parse_eew(data: dict) -> Optional[EEW]:
    try:
        return EEW(
            report_no=data["Serial"],
            title=data["Title"],
            report_time=data["AnnouncedTime"],

            hypo_name=data["Hypocenter"],
            magnitude=float(data.get("Magnitude") or data.get("Magunitude") or 0.0),
            depth=data.get("Depth", 0),
            max_shindo=data.get("MaxIntensity"),

            warn_area=data.get("WarnArea", []),

            is_sea=data.get("isSea", False),
            is_test=data.get("isTraining", False),
            is_plum=data.get("isAssumption", False),
            is_warn=data.get("isWarn", False),
            is_final=data.get("isFinal", False),
            is_cancel=data.get("isCancel", False),
        )

    except KeyError:
        return None
