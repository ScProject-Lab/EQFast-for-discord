from eew_bot.models.eew import EEW


def build_eew_embed(eew: EEW) -> dict:
    return {
        "embeds": [
            {
                "title": f"{eew.title} 第{eew.report_no}報" + " - 最終" if eew.is_final else "" + " - 取消" if eew.is_cancel else "",
                "description": f"{eew.hypo_name}で地震" + "強い揺れに警戒" if eew.is_warn else "" + f"M {eew.magnitude}\u3000深さ {eew.depth}km",
                "color": 0x9c0000 if eew.is_warn else 0xdb9d00,
                "fields": [
                    {"name": "推定最大震度", "value": eew.max_shindo, "inline": False},
                    {"name": "発表時刻", "value": eew.report_time, "inline": False},
                ]
            }
        ]
    }