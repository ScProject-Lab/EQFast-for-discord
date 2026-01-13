from typing import Dict, Any
from eew_bot.models.eew import EEW
from eew_bot.models.quake import EarthquakeEvent
from datetime import datetime


def build_eew_embed(eew: EEW) -> dict:
    kind = "警報" if eew.is_warn else "予報"
    final = " - 最終" if eew.is_final else ""

    title = f"緊急地震速報（{kind}） 第{eew.report_no}報{final}"

    warn_desc = ""

    if eew.is_plum:
        eew_method = " (PLUM法による予測)"
    else:
        eew_method = ""

    warn_area_text = ""
    if eew.is_warn:
        warn_area_text = build_warn_area_text(eew.warn_area)
        warn_desc = "\u3000強い揺れに警戒"

    return {
        "embeds": [
            {
                "title": title,
                "description": f"{eew.hypo_name}で地震{eew_method}{warn_desc}\nM {eew.magnitude}\u3000深さ {eew.depth}km",
                "color": 0x9C0000 if eew.is_warn else 0xDB9D00,
                "fields": [
                    {"name": "推定最大震度", "value": eew.max_shindo, "inline": False},
                    {"name": "対象地域", "value": warn_area_text, "inline": False},
                    {"name": "発表時刻", "value": eew.report_time, "inline": False},
                ]
            }
        ]
    }


def build_warn_area_text(warn_areas: list) -> str:
    if not warn_areas:
        return ""

    shindo_map = {}

    for area in warn_areas:
        shindo = area.get("Shindo1")
        chiiki = area.get("Chiiki")
        arrive_text = area.get("Arrive", "")

        if not shindo or not chiiki:
            continue

        suffix = arrive_suffix(arrive_text)

        shindo_map.setdefault(shindo, [])

        if not any(c == chiiki for c, _ in shindo_map[shindo]):
            shindo_map[shindo].append((chiiki, suffix))

    if not shindo_map:
        return ""

    text_lines = [""]

    shindo_order = ["7", "6強", "6弱", "5強", "5弱", "4", "3"]

    for shindo in shindo_order:
        areas = shindo_map.get(shindo)
        if not areas:
            continue

        text_lines.append(f"**[推定震度 {shindo}]**")

        area_texts = []
        for chiiki, suffix in areas:
            area_texts.append(f"{chiiki}{suffix}\n")

        text_lines.append("".join(area_texts))

    return "\n".join(text_lines)


def arrive_suffix(arrive_text: str) -> str:
    if not arrive_text:
        return ""

    if "既に到達" in arrive_text:
        return "（到達）"

    if "主要動到達時刻の予測なし" in arrive_text:
        return "（到達予測無し）"

    return ""


def build_quake_embed(quake: EarthquakeEvent) -> Dict[str, Any]:
    max_scale = quake.earthquake.max_scale
    if max_scale >= 50:
        color = 0xAD0202
    elif max_scale >= 40:
        color = 0xFF8000
    elif max_scale >= 30:
        color = 0xFFC400
    else:
        color = 0x00A6FF

    scale_map = {
        10: "1", 20: "2", 30: "3", 40: "4",
        45: "5弱", 50: "5強", 55: "6弱", 60: "6強", 70: "7"
    }
    max_scale_str = scale_map.get(max_scale, "不明")

    depth = quake.earthquake.hypocenter.depth

    if depth == 0:
        depth_str = "ごく浅い"
    elif depth == -1:
        depth_str = "不明"
    else:
        depth_str = f"{depth}km"

    tsunami_info = quake.earthquake.domestic_tsunami
    tsunami_text = {
        "None": "この地震による津波の心配はありません。",
        "Unknown": "津波の情報は不明です。今後の情報に注意してください。",
        "Checking": "津波などの詳しい情報は追ってお知らせします。",
        "NonEffective": "若干の海面変動があるかもしれませんが、被害の心配はありません。",
        "Watch": "現在、津波注意報を発表中です。",
        "Warning": "現在、津波予報等を発表中です。",
    }.get(tsunami_info, tsunami_info)

    magnitude = format_number(quake.earthquake.hypocenter.magnitude)

    raw_eq_time = datetime.strptime(quake.earthquake.time, "%Y/%m/%d %H:%M:%S")
    eq_time = raw_eq_time.strftime("%d日 %H:%M")

    quake_desc = f"{eq_time}頃、{quake.earthquake.hypocenter.name}で地震がありました。"
    quake_desc += tsunami_text

    fields = [
        {
            "name": "最大震度",
            "value": max_scale_str,
            "inline": False
        },
        {
            "name": "震源地",
            "value": quake.earthquake.hypocenter.name,
            "inline": True
        },
        {
            "name": "M",
            "value": magnitude,
            "inline": True
        },
        {
            "name": "深さ",
            "value": depth_str,
            "inline": True
        },
    ]

    if quake.points:
        points_text = build_intensity_text(quake.points, scale_map)
        fields.append({
            "name": "各地の震度",
            "value": points_text,
            "inline": False
        })

    fields.append({
        "name": "発生時刻",
        "value": eq_time,
        "inline": False
    })

    embed = {
        "title": "地震情報",
        "description": quake_desc,
        "color": color,
        "fields": fields,
        "footer": {
            "text": f"ソース\n{quake.issue.source}"
        }
    }

    return {"embeds": [embed]}


def build_intensity_text(points: list, scale_map: dict) -> str:
    if not points:
        return ""

    intensity_groups = {}
    for point in points:
        scale = scale_map.get(point.scale, "?")
        if scale not in intensity_groups:
            intensity_groups[scale] = []

        location = f"{point.pref}{point.addr}"
        if location not in intensity_groups[scale]:
            intensity_groups[scale].append(location)

    scale_order = ["7", "6強", "6弱", "5強", "5弱", "4", "3", "2", "1"]
    text_lines = []

    for scale in scale_order:
        if scale in intensity_groups:
            locations = intensity_groups[scale]
            text_lines.append(f"**<震度{scale}>**")

            location_text = "\u3000".join(locations)
            text_lines.append(location_text)

    return "\n".join(text_lines)


def format_number(n):
    if isinstance(n, int) or n == int(n):
        return f"{n:.1f}"
    else:
        return str(n)
