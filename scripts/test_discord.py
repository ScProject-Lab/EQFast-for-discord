import asyncio

from eew_bot.parsers.eew_parser import parse_eew
from eew_bot.utils.formatter import build_eew_embed, build_raw_text
from eew_bot.utils.webhook import send_webhook
from eew_bot.config import EMBED_WH, RAW_WH

dummy_data = {
    "type": "jma_eew",
    "Title": "緊急地震速報（予報）",
    "CodeType": "Ｍ、最大予測震度及び主要動到達予測時刻の緊急地震速報",
    "Issue": {
        "Source": "大阪",
        "Status": "通常"
    },
    "EventID": "20260308221821",
    "Serial": 5,
    "AnnouncedTime": "2026/03/08 22:18:51",
    "OriginTime": "2026/03/08 22:18:19",
    "Hypocenter": "岩手県内陸北部",
    "Latitude": 39.7,
    "Longitude": 141,
    "Magunitude": 1,
    "Depth": 10,
    "MaxIntensity": "4",
    "Accuracy": {
        "Epicenter": "P 波／S 波レベル超え、IPF 法（1 点）、または仮定震源要素",
        "Depth": "P 波／S 波レベル超え、IPF 法（1 点）、または仮定震源要素",
        "Magnitude": "P 波／S 波レベル超え、または仮定震源要素"
    },
    "MaxIntChange": {
        "String": "ほとんど変化なし",
        "Reason": "不明、未設定時、キャンセル時"
    },
    "WarnArea": [
        {
            "Chiiki": "岩手県内陸北部",
            "Shindo1": "4",
            "Shindo2": "不明",
            "Time": "221822",
            "Type": "予報",
            "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
        }
    ],
    "isSea": False,
    "isTraining": False,
    "isAssumption": True,
    "isWarn": False,
    "isFinal": True,
    "isCancel": False,
    "OriginalText": "36 04 00 260308221851 C11 260308221819 ND20260308221821 NCN905 JD////////////// JN005 212 N397 E1410 010 10 04 RK11811 RT/09// RC0//// EBI 212 S04// 221822 09 9999=",
    "Pond": "11"
}


async def main():
    eew = parse_eew(dummy_data)
    if eew is None:
        print("parse_eew returned None")
        return

    embed = build_eew_embed(eew)
    raw_text = build_raw_text(eew)

    print("Sending embed to EMBED_WH...")
    await send_webhook(EMBED_WH, embed)
    print("Embed sent successfully")

    print("Sending raw text to RAW_WH...")
    await send_webhook(RAW_WH, {"content": raw_text})
    print("Raw text sent successfully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
