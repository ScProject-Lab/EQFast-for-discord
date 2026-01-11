from eew_bot.models.eew import EEW


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
