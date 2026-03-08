import aiohttp
from eew_bot.utils.logger import logger


async def send_webhook(url: str | None, payload: dict):
    if not url:
        logger.error("Webhook URL is None")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status != 204:
                text = await resp.text()
                logger.error(f"webhook error {resp.status}: {text}")
