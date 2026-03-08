import os
from dotenv import load_dotenv

load_dotenv()

EMBED_WH = os.getenv("EMBED_WH")
RAW_WH = os.getenv("RAW_WH")
EEW_API_URL = os.getenv("EEW_API_URL")
QUAKE_API_URL = os.getenv("QUAKE_API_URL")
