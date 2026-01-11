import asyncio
import json
import websockets
import random


async def handler(ws):
    print("client connected")

    # heartbeat
    while True:
        await asyncio.sleep(2)

        if random.random() < 0.2:
            print("simulate disconnect")
            await ws.close()
            return

        msg = {
            "type": "heartbeat",
            "timestamp": asyncio.get_event_loop().time()
        }

        await ws.send(json.dumps(msg))


async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("ws test server started")
        await asyncio.Future()

asyncio.run(main())
