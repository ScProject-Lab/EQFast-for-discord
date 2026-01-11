import asyncio
import json
import websockets
import random


async def handler(ws):
    print("client connected")

    # heartbeat
    while True:
        await asyncio.sleep(2)

        if random.random() < 0.2:
            print("simulate disconnect")
            await ws.close()
            return

        msg = {
            "type": "jma_eew",
            "Title": "緊急地震速報（警報）",
            "CodeType": "Ｍ、最大予測震度及び主要動到達予測時刻の緊急地震速報",
            "Issue": {
                "Source": "東京",
                "Status": "通常"
            },
            "EventID": "20251208231519",
            "Serial": 29,
            "AnnouncedTime": "2025/12/08 23:16:07",
            "OriginTime": "2025/12/08 23:15:10",
            "Hypocenter": "青森県東方沖",
            "Latitude": 41,
            "Longitude": 142.2,
            "Magunitude": 7.2,
            "Depth": 60,
            "MaxIntensity": "6弱",
            "Accuracy": {
                "Epicenter": "IPF 法（5 点以上）",
                "Depth": "IPF 法（5 点以上）",
                "Magnitude": "全点全相"
            },
            "MaxIntChange": {
                "String": "ほとんど変化なし",
                "Reason": "不明、未設定時、キャンセル時"
            },
            "WarnArea": [
                {
                    "Chiiki": "青森県下北",
                    "Shindo1": "6弱",
                    "Shindo2": "5強",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "青森県三八上北",
                    "Shindo1": "6弱",
                    "Shindo2": "5強",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "青森県津軽北部",
                    "Shindo1": "5強",
                    "Shindo2": "5弱",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "渡島地方東部",
                    "Shindo1": "5強",
                    "Shindo2": "5弱",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "胆振地方中東部",
                    "Shindo1": "5強",
                    "Shindo2": "5強",
                    "Time": "231605",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "岩手県内陸北部",
                    "Shindo1": "5強",
                    "Shindo2": "5強",
                    "Time": "231537",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "岩手県沿岸北部",
                    "Shindo1": "5弱",
                    "Shindo2": "5弱",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "日高地方中部",
                    "Shindo1": "5弱",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "石狩地方中部",
                    "Shindo1": "5弱",
                    "Shindo2": "4",
                    "Time": "231610",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "青森県津軽南部",
                    "Shindo1": "5弱",
                    "Shindo2": "5弱",
                    "Time": "231600",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "日高地方東部",
                    "Shindo1": "5弱",
                    "Shindo2": "5弱",
                    "Time": "231602",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "石狩地方南部",
                    "Shindo1": "5弱",
                    "Shindo2": "5弱",
                    "Time": "231605",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "十勝地方南部",
                    "Shindo1": "5弱",
                    "Shindo2": "5弱",
                    "Time": "231607",
                    "Type": "警報",
                    "Arrive": "主要動到達時刻の予測なし（PLUM 法による予測）"
                },
                {
                    "Chiiki": "秋田県内陸北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "渡島地方西部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "岩手県沿岸南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "岩手県内陸南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "日高地方西部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "檜山地方",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "十勝地方中部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "胆振地方西部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "渡島地方北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "秋田県沿岸北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "秋田県沿岸南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "秋田県内陸南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "空知地方南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "十勝地方北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231609",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "石狩地方北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231612",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "後志地方北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231614",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "宮城県北部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231619",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "宮城県中部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231619",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "宮城県南部",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231632",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "福島県中通り",
                    "Shindo1": "4",
                    "Shindo2": "4",
                    "Time": "231640",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "後志地方東部",
                    "Shindo1": "4",
                    "Shindo2": "3",
                    "Time": "//////",
                    "Type": "警報",
                    "Arrive": "既に到達と予測"
                },
                {
                    "Chiiki": "後志地方西部",
                    "Shindo1": "4",
                    "Shindo2": "3",
                    "Time": "231613",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "釧路地方中南部",
                    "Shindo1": "4",
                    "Shindo2": "3",
                    "Time": "231616",
                    "Type": "警報",
                    "Arrive": "未到達"
                },
                {
                    "Chiiki": "山形県庄内",
                    "Shindo1": "4",
                    "Shindo2": "3",
                    "Time": "231624",
                    "Type": "警報",
                    "Arrive": "未到達"
                }
            ],
            "isSea": True,
            "isTraining": False,
            "isAssumption": False,
            "isWarn": True,
            "isFinal": False,
            "isCancel": False,
            "OriginalText": "37 03 00 251208231607 C11 251208231510 ND20251208231519 NCN029 JD////////////// JN/// 285 N410 E1422 060 72 6- RK44554 RT11/// RC0//// EBI 203 S6-5+ ////// 11 202 S6-5+ ////// 11 200 S5+5- ////// 11 106 S5+5- ////// 11 146 S5+5+ 231605 19 212 S5+5+ 231537 19 210 S5-5- ////// 11 151 S5-04 ////// 11 101 S5-04 231610 10 201 S5-5- 231600 19 152 S5-5- 231602 19 102 S5-5- 231605 19 157 S5-5- 231607 19 232 S0404 ////// 11 107 S0404 ////// 11 211 S0404 ////// 11 213 S0404 ////// 11 150 S0404 ////// 11 110 S0404 ////// 11 156 S0404 ////// 11 145 S0404 ////// 11 105 S0404 ////// 11 230 S0404 ////// 11 231 S0404 ////// 11 233 S0404 ////// 11 122 S0404 ////// 11 155 S0404 231609 10 100 S0404 231612 10 115 S0404 231614 10 220 S0404 231619 10 222 S0404 231619 10 221 S0404 231632 10 250 S0404 231640 10 116 S0403 ////// 11 117 S0403 231613 10 161 S0403 231616 10 240 S0403 231624 10 9999=",
            "Pond": "7"
        }

        await ws.send(json.dumps(msg))


async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("ws test server started")
        await asyncio.Future()

asyncio.run(main())
