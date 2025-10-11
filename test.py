import json
import aiohttp
import asyncio

# POSTするデータ
data = "地震情報自動送信テスト\n---地震情報---\n午前4時24分頃、三陸沖で地震がありました。この地震による津波の心配はありません。\n\n震源 三陸沖\n最大震度 5弱\n深さ 40km\nM None\n\n各地の震度\n震度5弱\n岩手県"

# JSONに変換（日本語をエスケープしない）
json_data = json.dumps(data, ensure_ascii=False)


async def post_eqinfo(json_data):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = "https://trigger.macrodroid.com/eb0021e1-7a69-45c7-aa90-1a5b489b2e7e/eqinfo"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json_data.encode("utf-8"), headers=headers) as response:
            print(response.status)
            text = await response.text()
            print(text)

if __name__ == "__main__":
    asyncio.run(post_eqinfo(json_data))
