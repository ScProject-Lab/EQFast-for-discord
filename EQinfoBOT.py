import websockets
import asyncio
import json
import logging
import aiohttp
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK")
macro_url = os.getenv("MACRO_WEBHOOK")

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


async def wsconnect(name, url):
    while True:
        try:
            async with websockets.connect(url) as websocket:
                logger.info(f"{name} connected")
                async for message in websocket:
                    try:
                        jsondata = json.loads(message)
                    except json.JSONDecodeError as e:
                        logger.error(f"{name} JSON parse error\n{e}")
                        continue

                    logger.debug(f"{name} data received: {jsondata}")

                    if name == "wolfx":
                        type = jsondata.get("type", "不明")

                        if type == "jma_eew":
                            isWarn = jsondata.get("isWarn", False)
                            Serial = jsondata.get("Serial", "不明")
                            Title = jsondata.get("Title", "不明")
                            Hypocenter = jsondata.get("Hypocenter", "不明")
                            Magunitude = jsondata.get("Magunitude", "不明")
                            Depth = jsondata.get("Depth", "不明")
                            AnnouncedTime = jsondata.get("AnnouncedTime", "不明")
                            MaxIntensity = jsondata.get("MaxIntensity", "不明")
                            isFinal = jsondata.get("isFinal", False)
                            isCancel = jsondata.get("isCancel", False)

                            logger.debug(f"{name}:{Title} 第{Serial}報")

                            if isWarn:
                                Title = f"{Title} 第{Serial}報"
                                if isFinal:
                                    Title += " - 最終"
                                if isCancel:
                                    Title += " - キャンセル報"

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

                                async with aiohttp.ClientSession() as session:
                                    async with session.post(webhook_url, json=message) as response:
                                        status = response.status

                                # Responseが200-299なら成功
                                if 200 <= status < 300:
                                    logger.info(f"{name} Discord webhook finished:{status}")
                                else:
                                    logger.warning(f"{name} Discord webhook failed (status={status})")

                            else:
                                Title = f"{Title} 第{Serial}報"
                                if isFinal:
                                    Title += " - 最終"
                                if isCancel:
                                    Title += " - キャンセル報"

                                message = {
                                    "embeds": [
                                        {
                                            "title": f"{Title}",
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
                                    async with session.post(webhook_url, json=message) as response:
                                        status = response.status

                                # Responseが200-299なら成功
                                if 200 <= status < 300:
                                    logger.info(f"{name} Discord webhook finished:{status}")
                                else:
                                    logger.warning(f"{name} Discord webhook failed | status:{status}")

                    elif name == "p2p":
                        code = jsondata.get("code", "不明")

                        if code == "551":
                            #  すべての情報取得
                            hyponame = jsondata["earthquake"]["hypocenter"]["name"]
                            time = jsondata["earthquake"]["time"]
                            maxscale_raw = str(jsondata["earthquake"]["maxScale"])
                            magnitude = str(jsondata["earthquake"]["hypocenter"]["magnitude"])
                            depth = str(jsondata["earthquake"]["hypocenter"]["depth"])
                            tsunami = jsondata["earthquake"]["domesticTsunami"]
                            source = jsondata["issue"]["source"]
                            type = jsondata["issue"]["type"]

                            send_str = ""
                            message = {}

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
                                "None": "この地震による津波の心配はありません。",
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

                            headers = {"Content-Type": "application/json; charset=utf-8"}

                            # ここのifは情報の種類を判定(震度速報etc...)
                            if type == "ScaleAndDestination":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "地震情報",
                                            "description": f"{time}頃、{hyponame}で地震がありました。\n{tsunami_info}",
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

                                send_str = f"---地震情報---\n{time}頃、{hyponame}で地震がありました。{tsunami_info}\n\n震源  {hyponame}\n最大震度  {maxscale}\n深さ  {depth}km\nM {magnitude}\n\n【各地の震度】\n開発中\n\nソース {source}\n[試験自動送信中]"

                            elif type == "ScalePrompt":
                                if depth == "-1":
                                    depth = "調査中"
                                elif depth == "0":
                                    depth = "ごく浅い"
                                else:
                                    depth = f"{depth}km"

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
                                                    "name": "震源",
                                                    "value": "調査中",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "M",
                                                    "value": "調査中",
                                                    "inline": True
                                                },
                                                {
                                                    "name": "深さ",
                                                    "value": f"{depth}",
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

                                send_str = f"---震度速報---\n{time}頃、最大震度{maxscale}の地震がありました。{tsunami_info}\n\n震源  調査中\n最大震度  {maxscale}\n深さ  調査中\nM {magnitude}\n\n【各地の震度】\n開発中\n\nソース {source}\n[試験自動送信中]"

                            elif type == "Destination":
                                message = {
                                    "embeds": [
                                        {
                                            "title": "震源に関する情報",
                                            "description": f"{time}頃、最大震度{maxscale}の地震がありました。\n{tsunami_info}",
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
                                                    "value": f"{depth}",
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
                                # ✅ どれにも当てはまらないとき
                                message = {"content": f"[未分類] type={type} の地震データを受信しました"}
                                send_str = f"[未分類] type={type} の地震データを受信しました"

                            print(send_str)

                            async with aiohttp.ClientSession() as session:
                                # Discord webhook送信
                                headers = {"Content-Type": "application/json"}
                                async with session.post(webhook_url, json=message, headers=headers) as response:
                                    d_status = response.status
                                    print(json.dumps(message, ensure_ascii=False, indent=2))

                            if 200 <= d_status < 300:
                                logger.info(f"{name} webhook finished")
                            else:
                                logger.warning(f"{name} webhook failed (d_status={d_status})")

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
