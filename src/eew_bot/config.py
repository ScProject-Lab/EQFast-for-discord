import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RAW_DATA_WH = os.getenv("RAW_D_WH")
EEW_API_URL = os.getenv("WOLFX_API")
QUAKE_API_URL = os.getenv("QUAKE_API_URL")
