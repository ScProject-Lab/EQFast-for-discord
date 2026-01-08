from eew_bot.models.eew import EEW


def build_eew_embed(eew: EEW) -> dict:
    title = f"{eew.title} 第{eew.report_no}報"
    if eew.is_final:
        title += " - 最終"
    if eew.is_cancel:
        title += " - 取消"

    desc = f"{eew.hypo_name}で地震\n"
    if eew.is_warn:
        desc += " 強い揺れに警戒\n"
    desc += f"M {eew.magnitude:.1f}\u3000深さ {eew.depth}km"

    return {
        "embeds": [
            {
                "title": title,
                "description": desc,
                "color": 0x9C0000 if eew.is_warn else 0xDB9D00,
                "fields": [
                    {"name": "推定最大震度", "value": eew.max_shindo, "inline": False},
                    {"name": "発表時刻", "value": eew.report_time, "inline": False},
                ]
            }
        ]
    }
