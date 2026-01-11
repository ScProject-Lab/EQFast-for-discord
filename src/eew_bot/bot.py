import asyncio
from eew_bot.services.eew_api import connect_eew
from eew_bot.utils.logger import logger


async def main():
    logger.info("EQFast bot started")
    try:
        await connect_eew()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        raise


def start():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
