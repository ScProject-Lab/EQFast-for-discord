import asyncio
import json
import sys
from pathlib import Path

from eew_bot.parsers.eew_parser import parse_eew
from eew_bot.utils.formatter import build_eew_embed, build_raw_text
from eew_bot.utils.webhook import send_webhook
from eew_bot.config import EMBED_WH, RAW_WH


def load_dummy_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


async def main():
    # コマンドライン引数 or デフォルトパス
    json_path = (
        sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "dummy.json"
    )

    dummy_data = load_dummy_data(json_path)

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
