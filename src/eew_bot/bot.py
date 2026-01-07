async def poll_eew():
    eew = await fetch_eew()
    if is_new_eew(eew):
        await send_eew(eew)

def start():
    