import websockets
import json
import asyncio
from typing import Optional

from eew_bot.config import EEW_API_URL
from eew_bot.utils.logger import logger
from eew_bot.parsers.eew_parser import parse_eew
from eew_bot.utils.discord_webhook import send_webhook
from eew_bot.utils.discord_formatter import build_eew_embed
from eew_bot.utils.discord_raw_webhook import send_raw_message
from eew_bot.utils.discord_raw_formatter import build_raw_text


async def process_eew_message(data: dict) -> None:
    try:
        eew = parse_eew(data)
        if eew is None:
            return

        logger.info(
            f"EEW | 震源 {eew.hypo_name} | M {eew.magnitude} | 最大震度 {eew.max_shindo}"
        )

        payload = build_eew_embed(eew)
        text = build_raw_text(eew)

        await asyncio.gather(
            send_webhook(payload),
            send_raw_message(text),
            return_exceptions=True
        )
    except Exception as e:
        logger.error(f"EEW処理エラー: {e}", exc_info=True)


async def handle_websocket_connection(websocket) -> None:
    logger.info("Connected to Wolfx")

    async for message in websocket:
        logger.debug(f"Raw message: {message}")

        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            logger.warning("Wolfx: JSON parse failed")
            continue

        msg_type = data.get("type")

        if msg_type == "heartbeat":
            logger.debug("heartbeat received")
            continue
        elif msg_type != "jma_eew":
            logger.debug(f"Ignored message type: {msg_type}")
            continue

        asyncio.create_task(process_eew_message(data))


async def connect_eew_with_retry(max_retries: Optional[int] = None) -> None:
    if EEW_API_URL is None:
        logger.error("Wolfx: URI is None")
        return

    retry_count = 0
    base_delay = 1
    max_delay = 60

    while max_retries is None or retry_count < max_retries:
        try:
            async with websockets.connect(
                EEW_API_URL,
                ping_interval=20,
                ping_timeout=10,
            ) as websocket:
                retry_count = 0
                await handle_websocket_connection(websocket)

        except websockets.exceptions.ConnectionClosed as e:
            logger.warning(f"WebSocket接続が切断されました: {e}")

        except websockets.exceptions.InvalidURI as e:
            logger.error(f"無効なURI: {EEW_API_URL} - {e}")
            break

        except Exception as e:
            logger.error(f"予期しないエラー: {e}", exc_info=True)

        retry_count += 1
        delay = min(base_delay * (2 ** (retry_count - 1)), max_delay)
        logger.info(f"再接続まで {delay} 秒待機... (試行回数: {retry_count})")
        await asyncio.sleep(delay)

    logger.error("最大再接続回数に達しました。プログラムを終了します。")


async def connect_eew():
    await connect_eew_with_retry(max_retries=None)
