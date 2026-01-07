from eew_bot.models.eew import EEW

def parse_eew(data: dict) -> EEW:
    return EEW(
        event_id=data["EventID"],
        report_no=data["Serial"],
        title=data["Title"],
        report_time=data["AnnouncedTime"],

        hypo_name=data["Hypocenter"],
        magnitude=data["Magnitude"],
        depth=data["Depth"],
        max_shindo=data.get("MaxIntensity"),

        warn_area=data.get("Warnarea", []),

        is_sea=data["isSea"],
        is_test=data["isTraining"],
        is_plum=data["isAssumption"],
        is_warn=data["isWarn"],
        is_final=data["isFinal"],
        is_cancel=data["isCancel"],
    )
