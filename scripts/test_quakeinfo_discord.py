import asyncio
import json
import sys
from pathlib import Path

from eew_bot.parsers.p2p_parser import parse_p2p_event
from eew_bot.utils.formatter import build_quake_embed, build_quake_raw_text
from eew_bot.utils.webhook import send_webhook
from eew_bot.config import EMBED_WH, RAW_WH


def load_dummy_data(path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


async def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "dummy_p2p.json"
    dummy_data = load_dummy_data(json_path)

    quake = parse_p2p_event(dummy_data)
    if quake is None:
        print("parse_p2p_event returned None")
        return

    embed = build_quake_embed(quake)
    raw_text = build_quake_raw_text(quake)

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