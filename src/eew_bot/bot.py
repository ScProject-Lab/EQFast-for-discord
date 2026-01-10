import asyncio
from eew_bot.services.eew_api import connect_eew
from eew_bot.utils.logger import logger


async def main():
    logger.info("EQFast bot started")

    while True:
        try:
            await connect_eew()
        except Exception as e:
            logger.exception(f"connect_eew crashed: {e}")

        logger.warning("EEW connection closed. Reconnecting in 5s...")
        await asyncio.sleep(5)


def start():
    asyncio.run(main())
