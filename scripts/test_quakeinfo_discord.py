import asyncio

from eew_bot.parsers.p2p_parser import parse_p2p_event
from eew_bot.utils.formatter import build_quake_embed, build_quake_raw_text
from eew_bot.utils.webhook import send_webhook
from eew_bot.config import EMBED_WH, RAW_WH

# P2P地震情報API レスポンスデータ（海外地震情報）
dummy_data = {
    "code": 551,
    "created_at": "2024/01/01 23:06:23.401",
    "earthquake": {
        "domesticTsunami": "Checking",
        "foreignTsunami": "Unknown",
        "hypocenter": {
            "depth": -1,
            "latitude": -200,
            "longitude": -200,
            "magnitude": -1,
            "name": "",
        },
        "maxScale": 70,
        "time": "2024/01/01 23:03:00",
    },
    "id": "6592c6dff0f6de0007564ec2",
    "issue": {
        "correct": "None",
        "source": "気象庁",
        "time": "2024/01/01 23:05:48",
        "type": "ScalePrompt",
    },
    "points": [
        {"addr": "石川県能登", "isArea": True, "pref": "石川県", "scale": 70},
        {"addr": "石川県加賀", "isArea": True, "pref": "石川県", "scale": 50},
        {"addr": "新潟県中越", "isArea": True, "pref": "新潟県", "scale": 55},
        {"addr": "新潟県上越", "isArea": True, "pref": "新潟県", "scale": 50},
        {"addr": "新潟県下越", "isArea": True, "pref": "新潟県", "scale": 50},
        {"addr": "新潟県佐渡", "isArea": True, "pref": "新潟県", "scale": 50},
        {"addr": "富山県東部", "isArea": True, "pref": "富山県", "scale": 50},
        {"addr": "富山県西部", "isArea": True, "pref": "富山県", "scale": 50},
        {"addr": "福井県嶺北", "isArea": True, "pref": "福井県", "scale": 50},
        {"addr": "福井県嶺南", "isArea": True, "pref": "福井県", "scale": 40},
        {"addr": "長野県北部", "isArea": True, "pref": "長野県", "scale": 45},
        {"addr": "長野県中部", "isArea": True, "pref": "長野県", "scale": 40},
        {"addr": "長野県南部", "isArea": True, "pref": "長野県", "scale": 40},
        {"addr": "岐阜県飛騨", "isArea": True, "pref": "岐阜県", "scale": 45},
        {"addr": "岐阜県美濃東部", "isArea": True, "pref": "岐阜県", "scale": 40},
        {"addr": "岐阜県美濃中西部", "isArea": True, "pref": "岐阜県", "scale": 40},
        {"addr": "山形県庄内", "isArea": True, "pref": "山形県", "scale": 40},
        {"addr": "山形県村山", "isArea": True, "pref": "山形県", "scale": 40},
        {"addr": "山形県置賜", "isArea": True, "pref": "山形県", "scale": 40},
        {"addr": "山形県最上", "isArea": True, "pref": "山形県", "scale": 30},
        {"addr": "福島県中通り", "isArea": True, "pref": "福島県", "scale": 40},
        {"addr": "福島県会津", "isArea": True, "pref": "福島県", "scale": 40},
        {"addr": "福島県浜通り", "isArea": True, "pref": "福島県", "scale": 30},
        {"addr": "茨城県北部", "isArea": True, "pref": "茨城県", "scale": 40},
        {"addr": "茨城県南部", "isArea": True, "pref": "茨城県", "scale": 30},
        {"addr": "栃木県北部", "isArea": True, "pref": "栃木県", "scale": 40},
        {"addr": "栃木県南部", "isArea": True, "pref": "栃木県", "scale": 30},
        {"addr": "群馬県北部", "isArea": True, "pref": "群馬県", "scale": 40},
        {"addr": "群馬県南部", "isArea": True, "pref": "群馬県", "scale": 30},
        {"addr": "埼玉県北部", "isArea": True, "pref": "埼玉県", "scale": 40},
        {"addr": "埼玉県南部", "isArea": True, "pref": "埼玉県", "scale": 30},
        {"addr": "静岡県西部", "isArea": True, "pref": "静岡県", "scale": 40},
        {"addr": "静岡県東部", "isArea": True, "pref": "静岡県", "scale": 30},
        {"addr": "静岡県中部", "isArea": True, "pref": "静岡県", "scale": 30},
        {"addr": "愛知県西部", "isArea": True, "pref": "愛知県", "scale": 40},
        {"addr": "愛知県東部", "isArea": True, "pref": "愛知県", "scale": 30},
        {"addr": "三重県北部", "isArea": True, "pref": "三重県", "scale": 40},
        {"addr": "三重県中部", "isArea": True, "pref": "三重県", "scale": 30},
        {"addr": "三重県南部", "isArea": True, "pref": "三重県", "scale": 30},
        {"addr": "滋賀県北部", "isArea": True, "pref": "滋賀県", "scale": 40},
        {"addr": "滋賀県南部", "isArea": True, "pref": "滋賀県", "scale": 40},
        {"addr": "京都府南部", "isArea": True, "pref": "京都府", "scale": 40},
        {"addr": "京都府北部", "isArea": True, "pref": "京都府", "scale": 30},
        {"addr": "大阪府北部", "isArea": True, "pref": "大阪府", "scale": 40},
        {"addr": "大阪府南部", "isArea": True, "pref": "大阪府", "scale": 30},
        {"addr": "兵庫県北部", "isArea": True, "pref": "兵庫県", "scale": 40},
        {"addr": "兵庫県南東部", "isArea": True, "pref": "兵庫県", "scale": 30},
        {"addr": "兵庫県淡路島", "isArea": True, "pref": "兵庫県", "scale": 30},
        {"addr": "奈良県", "isArea": True, "pref": "奈良県", "scale": 40},
        {"addr": "鳥取県東部", "isArea": True, "pref": "鳥取県", "scale": 40},
        {"addr": "鳥取県中部", "isArea": True, "pref": "鳥取県", "scale": 30},
        {"addr": "鳥取県西部", "isArea": True, "pref": "鳥取県", "scale": 30},
        {"addr": "岩手県内陸北部", "isArea": True, "pref": "岩手県", "scale": 30},
        {"addr": "宮城県北部", "isArea": True, "pref": "宮城県", "scale": 30},
        {"addr": "宮城県南部", "isArea": True, "pref": "宮城県", "scale": 30},
        {"addr": "宮城県中部", "isArea": True, "pref": "宮城県", "scale": 30},
        {"addr": "秋田県沿岸北部", "isArea": True, "pref": "秋田県", "scale": 30},
        {"addr": "秋田県沿岸南部", "isArea": True, "pref": "秋田県", "scale": 30},
        {"addr": "秋田県内陸北部", "isArea": True, "pref": "秋田県", "scale": 30},
        {"addr": "秋田県内陸南部", "isArea": True, "pref": "秋田県", "scale": 30},
        {"addr": "千葉県北東部", "isArea": True, "pref": "千葉県", "scale": 30},
        {"addr": "千葉県北西部", "isArea": True, "pref": "千葉県", "scale": 30},
        {"addr": "千葉県南部", "isArea": True, "pref": "千葉県", "scale": 30},
        {"addr": "東京都２３区", "isArea": True, "pref": "東京都", "scale": 30},
        {"addr": "神奈川県東部", "isArea": True, "pref": "神奈川県", "scale": 30},
        {"addr": "神奈川県西部", "isArea": True, "pref": "神奈川県", "scale": 30},
        {"addr": "山梨県中・西部", "isArea": True, "pref": "山梨県", "scale": 30},
        {"addr": "山梨県東部・富士五湖", "isArea": True, "pref": "山梨県", "scale": 30},
        {"addr": "和歌山県北部", "isArea": True, "pref": "和歌山県", "scale": 30},
        {"addr": "島根県東部", "isArea": True, "pref": "島根県", "scale": 30},
        {"addr": "島根県隠岐", "isArea": True, "pref": "島根県", "scale": 30},
        {"addr": "岡山県北部", "isArea": True, "pref": "岡山県", "scale": 30},
        {"addr": "岡山県南部", "isArea": True, "pref": "岡山県", "scale": 30},
        {"addr": "徳島県北部", "isArea": True, "pref": "徳島県", "scale": 30},
        {"addr": "香川県東部", "isArea": True, "pref": "香川県", "scale": 30},
    ],
    "time": "2024/01/01 23:05:50.501",
    "timestamp": {
        "convert": "2024/01/01 23:05:50.497",
        "register": "2024/01/01 23:05:50.501",
    },
    "user_agent": "jmaxml-seis-parser-go, relay, register-api",
    "ver": "20231023",
}


async def main():
    quake = parse_p2p_event(dummy_data)
    if quake is None:
        print("parse_p2p_event returned None")
        return

    embed = build_quake_embed(quake)
    raw_text = build_quake_raw_text(quake)

    print("Sending embed to EMBED_WH...")
    await send_webhook(EMBED_WH, embed)
    print("Embed sent successfully")

    print("Sending raw text to RAW_WH...")
    await send_webhook(RAW_WH, {"content": raw_text})
    print("Raw text sent successfully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
