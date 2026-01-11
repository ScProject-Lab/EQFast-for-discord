from typing import Optional
from eew_bot.models.quake import (
    EarthquakeEvent,
    Earthquake,
    Hypocenter,
    Issue,
    Point,
)


def parse_p2p_event(data: dict) -> Optional[EarthquakeEvent]:
    if "earthquake" not in data:
        return None

    issue_raw = data.get("issue", {})
    issue = Issue(
        source=issue_raw.get("source", ""),
        correct=issue_raw.get("correct", ""),
        type=issue_raw.get("type", ""),
    )

    hypo_raw = data["earthquake"].get("hypocenter", {})
    hypocenter = Hypocenter(
        name=hypo_raw.get("name", ""),
        depth=hypo_raw.get("depth", -1),
        magnitude=hypo_raw.get("magnitude", 0.0),
        maxScale=hypo_raw.get("maxScale", 0),
    )

    eq_raw = data["earthquake"]
    earthquake = Earthquake(
        time=eq_raw.get("time", ""),
        max_scale=eq_raw.get("maxScale", 0),
        domestic_tsunami=eq_raw.get("domesticTsunami", ""),
        foreign_tsunami=eq_raw.get("foreignTsunami", ""),
        hypocenter=hypocenter,
    )

    points = []
    for p in data.get("points", []):
        points.append(
            Point(
                addr=p.get("addr", ""),
                is_area=p.get("isArea", False),
                pref=p.get("pref", ""),
                scale=p.get("scale", 0),
            )
        )

    return EarthquakeEvent(
        id=data.get("id", ""),
        code=data.get("code", 0),
        issue=issue,
        earthquake=earthquake,
        points=points,
    )