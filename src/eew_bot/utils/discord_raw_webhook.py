import aiohttp
from eew_bot.config import RAW_DATA_WH
from eew_bot.utils.logger import logger


async def send_raw_message(text: str):
    if not RAW_DATA_WH:
        logger.error("Raw data webhook URL is None")
        return

    payload = {
        "content": text
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(RAW_DATA_WH, json=payload) as resp:
            if resp.status != 204:
                body = await resp.text()
                logger.error(f"Raw data webhook error {resp.status}: {body}")
