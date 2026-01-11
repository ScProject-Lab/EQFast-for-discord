import websockets
import json

from eew_bot.config import P2P_API_URL
from eew_bot.utils.logger import logger
from eew_bot.parsers.p2p_parser import parse_p2p_event


async def connect_p2pquake():
    if P2P_API_URL is None:
        logger.error("P2P: URI is None")
        return

    try:
        async with websockets.connect(P2P_API_URL) as websocket:
            logger.debug("Connecte to P2P")

            async for message in websocket:
                logger.debug(f"Raw message: {message}")

                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    logger.warning("P2P: JSON parse failed")
                    continue

    except:
        and
