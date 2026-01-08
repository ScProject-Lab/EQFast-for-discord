import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RAW_DATA_WH = os.getenv("RAW_D_WH")
EEW_API_URL = os.getenv("WOLFX_API")
P2P_API_URL = os.getenv("P2P_API_URL")
