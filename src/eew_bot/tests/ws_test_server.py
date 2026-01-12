import asyncio
import json
import websockets
import random


async def handler(ws):
    print("client connected")

    while True:
        await asyncio.sleep(5)

        if random.random() < 0.2:
            print("simulate disconnect")
            await ws.close()
            return

        msg = {
            "id": "5ee1681202add671a1e1ae39",
            "time": "2019/08/26 21:04:06.958",
            "code": 551,
            "issue": {
                "source": "気象庁",
                "time": "2019/08/26 20:57:00",
                "correct": "None",
                "type": "DetailScale"
            },
            "earthquake": {
                "domesticTsunami": "Warning",
                "foreignTsunami": "Unknown",
                "hypocenter": {
                    "depth": 0,
                    "latitude": 24.4,
                    "longitude": 125.2,
                    "magnitude": 4,
                    "name": "宮古島近海"
                },
                "maxScale": 10,
                "time": "2019/08/26 20:53:00"
            },
            "points": [
                {
                    "addr": "宮古島市城辺福北",
                    "isArea": False,
                    "pref": "沖縄県",
                    "scale": 10
                },
                {
                    "addr": "宮古島市伊良部長浜",
                    "isArea": False,
                    "pref": "沖縄県",
                    "scale": 10
                }
            ],
            "comments": {
                "freeFormComment": ""
            }
        }

        await ws.send(json.dumps(msg))


async def main():
    async with websockets.serve(handler, "127.0.0.1", 3546):
        print("ws test server started")
        await asyncio.Future()

asyncio.run(main())
