import aiohttp
import websockets
import asyncio
from eew_bot.models.eew import EEW
from eew_bot.config import EEW_API_URL
from eew_bot.

async def fetch_eew(websocket):
    async for message in websocket:
        