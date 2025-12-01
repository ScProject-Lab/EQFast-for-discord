import asyncio
import logging
import websockets
import aiohttp
import json
import os
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler("bot.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

load_dotenv()

discordwh_url = os.getenv("DISCORD_WEBHOOK")

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

wolfxurl = "wss://ws-api.wolfx.jp/jma_eew"
p2purl = "wss://api.p2pquake.net/v2/ws"

headers = {'Content-Type': 'application/json'}


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

                        if type == "jma_eew":
                            isWarn = parsed_json.get("isWarn", False)
                            Serial = parsed_json.get("Serial", "不明")
                            Title = parsed_json.get("Title", "不明")
                            Hypocenter = parsed_json.get("Hypocenter", "不明")
                            Magunitude = parsed_json.get("Magunitude", "不明")
                            Depth = parsed_json.get("Depth", "不明")
                            AnnouncedTime = parsed_json.get("AnnouncedTime", "不明")
                            MaxIntensity = parsed_json.get("MaxIntensity", "不明")
                            isFinal = parsed_json.get("isFinal", False)
                            isCancel = parsed_json.get("isCancel", False)

                            logger.info(f"{name}:{Title} 第{Serial}報")

                            wh_title = f"{Title} 第{Serial}報"
                            if isFinal:
                                wh_title += " - 最終"
                            if isCancel:
                                wh_title += "- 取消"

                            if isWarn:
                                message = {
                                    "embeds": [
                                        {
                                            "title": f"{Title}",
                                            "color": 0xb2002f,
                                            "description": f"{Hypocenter}で地震\u3000身の安全を確保してください\nM{Magunitude}\u3000深さ{Depth}km",
                                            "fields": [
                                                {
                                                    "name": "推定最大震度",
                                                    "value": f"{MaxIntensity}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "発表時刻",
                                                    "value": f"{AnnouncedTime}",
                                                    "inline": False
                                                }
                                            ]

                                        }
                                    ]
                                }

                            else:
                                message = {
                                    "embeds": [
                                        {
                                            "title": f"{wh_title}",
                                            "color": 0xccb100,
                                            "description": f"{Hypocenter}で地震\nM{Magunitude}\u3000深さ{Depth}km",
                                            "fields": [
                                                {
                                                    "name": "推定最大震度",
                                                    "value": f"{MaxIntensity}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "発表時刻",
                                                    "value": f"{AnnouncedTime}",
                                                    "inline": False
                                                }
                                            ]

                                        }
                                    ]
                                }

                            async with aiohttp.ClientSession() as session:
                                async with session.post(discordwh_url, json=message) as response:
                                    status = response.status

                            # Responseが200-299なら成功
                            if 200 <= status < 300:
                                logger.info(f"{name} Discord webhook finished:{status}")
                            else:
                                logger.warning(f"{name} Discord webhook failed (status={status})")

                        elif type == "不明":
                            logger.warning(f"{name} unknown data type received")

                    elif name == "p2p":
                        code = parsed_json.get("code", None)

                        if code == 551:
                            hyponame = parsed_json["earthquake"]["hypocenter"]["name"]
                            time = parsed_json["earthquake"]["time"]
                            maxscale_raw = str(parsed_json["earthquake"]["maxScale"])
                            magnitude = str(parsed_json["earthquake"]["hypocenter"]["magnitude"])
                            depth = str(parsed_json["earthquake"]["hypocenter"]["depth"])
                            tsunami = parsed_json["earthquake"]["domesticTsunami"]
                            source = parsed_json["issue"]["source"]
                            type = parsed_json["issue"]["type"]

                            ms = {
                                "-1": "None",
                                "10": "1",
                                "20": "2",
                                "30": "3",
                                "40": "4",
                                "45": "5-",
                                "50": "5+",
                                "55": "6-",
                                "60": "6+",
                                "70": "7",
                            }

                            maxscale = ms[maxscale_raw]

                            if hyponame == "":
                                hyponame = "None"

                            if magnitude == "-1":
                                magnitude = "None"

                            tsunamistr = {
                                " ": "この地震による津波の心配はありません。",
                                "Unknown": "津波に関する情報は不明です。",
                                "Checking": "現在津波の情報を調査中です。",
                                "NonEffective": "若干の海面変動があるかも知れませんが、被害の心配はありません。",
                                "Watch": "現在、津波注意報が発表されています。",
                                "Warning": "現在、津波予報等を発表中です。"
                            }

                            tsunami_info = tsunamistr[tsunami]

                            # timeの秒を削除
                            time = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
                            time = time.strftime("%d日 %H:%M")

                            if type == "ScalePrompt":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "震度速報",
                                            "description": f"{time}頃、最大震度{maxscale}の地震がありました。\n{tsunami_info}",
                                            "color": 0x007cbf,
                                            "fields": [
                                                {
                                                    "name": "最大震度",
                                                    "value": f"{maxscale}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "発生時刻",
                                                    "value": f"{time}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "ソース",
                                                    "value": f"{source}",
                                                    "inline": False
                                                }
                                            ]
                                        }
                                    ]
                                }

                            elif type == "Destination":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "震源に関する情報",
                                            "description": f"{time}頃、{hyponame}で地震がありました。\n{tsunami_info}",
                                            "color": 0x007cbf,
                                            "fields": [
                                                {
                                                    "name": "震源",
                                                    "value": f"{hyponame}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "M",
                                                    "value": f"{magnitude}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "深さ",
                                                    "value": f"{depth}km",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "発生時刻",
                                                    "value": f"{time}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "ソース",
                                                    "value": f"{source}",
                                                    "inline": False
                                                }
                                            ]
                                        }
                                    ]
                                }

                            elif type == "ScaleAndDestination":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "震度·震源に関する情報",
                                            "description": f"{time}頃、{hyponame}で最大震度{maxscale}の地震がありました。\n{tsunami_info}",
                                            "color": 0x007cbf,
                                            "fields": [
                                                {
                                                    "name": "最大震度",
                                                    "value": f"{maxscale}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "震源",
                                                    "value": f"{hyponame}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "M",
                                                    "value": f"{magnitude}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "深さ",
                                                    "value": f"{depth}km",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "発生時刻",
                                                    "value": f"{time}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "ソース",
                                                    "value": f"{source}",
                                                    "inline": False
                                                }
                                            ]
                                        }
                                    ]
                                }

                            elif type == "Foreign":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "遠地地震に関する情報",
                                            "description": f"{time}頃、海外で大きな地震がありました。\n{tsunami_info}",
                                            "color": 0xd19e26,
                                            "fields": [
                                                {
                                                    "name": "震源",
                                                    "value": f"{hyponame}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "M",
                                                    "value": f"{magnitude}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "深さ",
                                                    "value": f"{depth}km",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "発生時刻",
                                                    "value": f"{time}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "ソース",
                                                    "value": f"{source}",
                                                    "inline": False
                                                }
                                            ]
                                        }
                                    ]
                                }

                            elif type == "DetailScale":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "地震情報",
                                            "description": f"{time}頃、{hyponame}で最大震度{maxscale}の地震がありました。\n{tsunami_info}",
                                            "color": 0x007cbf,
                                            "fields": [
                                                {
                                                    "name": "最大震度",
                                                    "value": f"{maxscale}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "震源",
                                                    "value": f"{hyponame}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "M",
                                                    "value": f"{magnitude}",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "深さ",
                                                    "value": f"{depth}km",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "発生時刻",
                                                    "value": f"{time}",
                                                    "inline": False
                                                },
                                                {
                                                    "name": "ソース",
                                                    "value": f"{source}",
                                                    "inline": False
                                                }
                                            ]
                                        }
                                    ]
                                }

                            else:
                                message = {"content": f"その他のメッセージ:{type}"}

                            async with aiohttp.ClientSession() as session:
                                async with session.post(discordwh_url, json=message) as response:
                                    status = response.status

                            # Responseが200-299なら成功
                            if 200 <= status < 300:
                                logger.info(f"{name} Discord webhook finished:{status}")
                            else:
                                logger.warning(f"{name} Discord webhook failed (status={status})")

        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"{name} disconnected\n{e}")

        except Exception as e:
            logger.error(f"{name} error:{e}")

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
