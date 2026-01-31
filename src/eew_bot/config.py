import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RAW_DATA_WH = os.getenv("RAW_DATA_WH")
EEW_API_URL = os.getenv("EEW_API_URL")
QUAKE_API_URL = os.getenv("QUAKE_API_URL")
