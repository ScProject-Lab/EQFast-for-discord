import json
import requests
import time
import sys
import pyperclip

# テスト用
with open("noto.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)


grade_translate = {
    "MajorWarning": "🟪大津波警報",
    "Warning": "🟥津波警報",
    "Watch": "🟨津波注意報",
    "Unknown": "不明",
}

p2p_url = "https://api.p2pquake.net/v2/jma/tsunami"
comparison = ""


def rq(p2p_url):
    areas = []
    levels = []
    immediate = []
    maxheight = []

    """
    json_data = requests.get(p2p_url)
    json_data = json.dumps(json_data.json())
    json_data = json.loads(json_data)
    """

    for i in range(len(json_data[0]["areas"])):
        time = json_data[0]["issue"]["time"]
        levels.append(grade_translate[json_data[0]["areas"][i]["grade"]])
        areas.append(json_data[0]["areas"][i]["name"])
        immediate.append(json_data[0]["areas"][i]["immediate"])
        maxheight.append(json_data[0]["areas"][i]["maxHeight"]["description"])

    if levels:

        previous = ""
        output = ""

        output += (f"{time} 発表\n")
        if levels[0] == "🟪大津波警報":
            output += "津波情報が発表されました。\n- 🟪大津波警報等が発表されました。今すぐ高台に避難してください。\n"
        elif levels[0] == "🟥津波警報":
            output += "津波情報が発表されました。\n- 🟥津波警報等が発表されました。今すぐ避難してください。\n"
        elif levels[0] == "🟨津波注意報":
            output += "津波情報が発表されました。\n- 🟨津波注意報等が発表されました。海岸から離れてください。\n"
        else:
            output += "津波情報が発表されました。\n詳細な情報が入り次第お知らせします。\n"
        for i in range(len(levels)):
            if previous == levels[i]:
                if immediate[i] == "true":
                    output += (f"  {areas[i]}  {maxheight[i]} すぐ来る\n")
                else:
                    output += (f"  {areas[i]}  {maxheight[i]}\n")
            else:
                output += (f"\n{levels[i]}\n")
                output += (f"  {areas[i]}  {maxheight[i]}\n")

            previous = levels[i]

        output += ("\nソース：気象庁・P2P地震情報 開発者向けAPI")

        return output


if __name__ == "__main__":
    try:
        while True:
            now = rq(p2p_url)
            if now != comparison:
                comparison = now
                print(comparison)
            pyperclip.copy(now)
            time.sleep(5)
    except KeyboardInterrupt:
        print("SHUTDOWN")
        sys.exit(0)
