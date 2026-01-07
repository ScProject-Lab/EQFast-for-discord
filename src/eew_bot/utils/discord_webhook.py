import aiohttp
from eew_bot.config import DISCORD_TOKEN
from eew_bot.utils.logger import logger


async def send_webhook(payload: dict):
    if not DISCORD_TOKEN:
        logger.error("Webhook URL is None")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(DISCORD_TOKEN, json=payload) as resp:
            if resp.status != 204:
                text = await resp.text()
                logger.error(f"webhook error {resp.status}: {text}")