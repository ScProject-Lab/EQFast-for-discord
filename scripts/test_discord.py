import asyncio

from eew_bot.parsers.eew_parser import parse_eew
from eew_bot.utils.formatter import build_eew_embed, build_raw_text
from eew_bot.utils.webhook import send_webhook
from eew_bot.config import EMBED_WH, RAW_WH

dummy_data = {
  "Title": "緊急地震速報（予報）",
  "CodeType": "Ｗ、警報、最大予測震度及び主要動到達予測時刻",
  "Issue": {
    "Source": "東京",
    "Status": "通常"
  },
  "EventID": "20260209170500_1",
  "Serial": 1,
  "AnnouncedTime": "2011/03/11 14:48:11",
  "OriginTime": "2011/03/11 14:48:10",
  "Hypocenter": "東北地方",
  "Latitude": 38.1,
  "Longitude": 142.9,
  "Magunitude": 1.0,
  "Depth": 10,
  "MaxIntensity": "5弱",
  "Accuracy": {
    "Epicenter": "IPF 法（5 点以上）",
    "Depth": "IPF 法（5 点以上）",
    "Magnitude": "全点全相"
  },
  "MaxIntChange": {
    "String": "増大",
    "Reason": "巨大地震による再計算"
  },
  "WarnArea": [],
  "isSea": False,
  "isTraining": False,
  "isAssumption": True,
  "isWarn": False,
  "isFinal": False,
  "isCancel": False
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
