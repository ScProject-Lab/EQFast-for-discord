import time

async def retry(func, times=3):
    time.sleep(times)