import asyncio
import logging
import websockets
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler("bot.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

wolfxurl = "wss://ws-api.wolfx.jp/jma_eew"
p2purl = "wss://api.p2pquake.net/v2/ws"

async def wsconnect(name, url):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                logger.info(f"{name} successfully connected")
                async for message in websocket:
                    try:
                        parsed_json = json.loads(message)
                    except json.JSONDecodeError as e:
                        logger.error(f"{name} JSON parse error:\n{e}")
                        continue

                    logger.debug(f"{name} data received: {message}")

                if name == "wolfx":
                    type = parsed_json.get("type", "不明")

                    if type == "eew":
                        


        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"{name} disconnected\n{e}")

        except Exception as e:
            logger.error(f"{name} error\n{e}")

        logger.warning(f"{name} disconnected, retrying...")
        await asyncio.sleep(2)



async def main():
    wolfxurl = "wss://ws-api.wolfx.jp/jma_eew"
    p2purl = "wss://api.p2pquake.net/v2/ws"
    await asyncio.gather(
        wsconnect("wolfx", wolfxurl),
        wsconnect("p2p", p2purl),
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("SHUTDOWN TRYING")
    finally:
        logger.info("SHUTDOWN FINISHED")