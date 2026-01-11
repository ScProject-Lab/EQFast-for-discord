import websockets
import json
import asyncio
from typing import Optional

from eew_bot.config import QUAKE_API_URL
from eew_bot.utils.logger import logger
from eew_bot.parsers.p2p_parser import parse_p2p_event
from eew_bot.utils.discord_webhook import send_webhook
from eew_bot.utils.discord_formatter import build_quake_embed
from eew_bot.utils.discord_raw_webhook import send_raw_message
from eew_bot.utils.discord_raw_formatter import build_quake_raw_text


async def process_quake_message(data: dict) -> None:
    try:
        quake = parse_p2p_event(data)
        if quake is None:
            return

        logger.info(
            f"地震情報 | 震源 {quake.earthquake.hypocenter.name} | "
            f"M {quake.earthquake.hypocenter.magnitude} | "
            f"最大震度 {quake.earthquake.max_scale}"
        )

        payload = build_quake_embed(quake)
        text = build_quake_raw_text(quake)

        await asyncio.gather(
            send_webhook(payload),
            send_raw_message(text),
            return_exceptions=True
        )
    except Exception as e:
        logger.error(f"地震情報処理エラー: {e}", exc_info=True)


async def handle_websocket_connection(websocket) -> None:
    logger.info("Connected to P2P Earthquake API")

    async for message in websocket:
        logger.debug(f"Raw message: {message}")

        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            logger.warning("P2P API: JSON parse failed")
            continue

        code = data.get("code")

        if code != 551:
            logger.debug(f"Ignored message code: {code}")
            continue

        asyncio.create_task(process_quake_message(data))


async def connect_quake_with_retry(max_retries: Optional[int] = None) -> None:
    if QUAKE_API_URL is None:
        logger.error("P2P API: URI is None")
        return

    retry_count = 0
    base_delay = 1
    max_delay = 60

    while max_retries is None or retry_count < max_retries:
        try:
            async with websockets.connect(
                QUAKE_API_URL,
                ping_interval=20,
                ping_timeout=10,
            ) as websocket:
                retry_count = 0
                await handle_websocket_connection(websocket)

        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"WebSocket接続が切断されました: {e}")

        except websockets.exceptions.InvalidURI as e:
            logger.error(f"無効なURI: {QUAKE_API_URL} - {e}")
            break

        except Exception as e:
            logger.error(f"予期しないエラー: {e}", exc_info=True)

        retry_count += 1
        delay = min(base_delay * (2 ** (retry_count - 1)), max_delay)
        logger.info(f"再接続まで {delay} 秒待機... (試行回数: {retry_count})")
        await asyncio.sleep(delay)

    logger.error("最大再接続回数に達しました。")


async def connect_quake():
    await connect_quake_with_retry(max_retries=None)
