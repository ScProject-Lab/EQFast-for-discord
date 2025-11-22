import requests
import dotenv
import os

dotenv.load_dotenv()

macro_url = os.getenv("LINE_MACRO")
line_send_data = "Test message from PYTHON"

with requests.post(macro_url, json={"message": line_send_data}) as response:
    response = response.status_code
    if 200 <= response < 300:
        print(f"{response} post finished")
    else:
        print(f"{response} post failed")
