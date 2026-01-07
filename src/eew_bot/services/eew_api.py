import websockets
import json

from eew_bot.config import EEW_API_URL
from eew_bot.utils.logger import logger
from eew_bot.parsers.eew_parser import parse_eew
from eew_bot.utils.discord_webhook import send_webhook
from eew_bot.utils.discord_formatter import build_eew_embed
from eew_bot.utils.discord_raw_webhook import send_raw_message
from eew_bot.utils.discord_raw_formatter import build_raw_text

from typing import Optional

async def connect_eew():
    if EEW_API_URL is None:
        logger.error("URI is None")
        return

    try:
        async with websockets.connect(EEW_API_URL) as websocket:
            logger.info(f"Connected to Wolfx")

            async for message in websocket:
                logger.debug(f"Raw message: {message}")

                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    logger.warning("JSON parse failed")
                    continue

                eew = parse_eew(data)
                if eew is None:
                    continue
                
                logger.info(
                    f"EEW {eew.event_id} | 震源地 {eew.hypo_name} | M {eew.magnitude} | 最大震度 {eew.max_shindo}"
                )

                eew = parse_eew(data)
                if eew is None:
                    continue

                payload = build_eew_embed(eew)
                await send_webhook(payload)

                text = build_raw_text(eew)
                await send_raw_message(text)

    except Exception as e:
        logger.error(f"Connect error: {e}")

