import requests
import xml.etree.ElementTree as ET
import json

# 気象庁のフィードURL
url = "https://www.data.jma.go.jp/developer/xml/feed/extra.xml"

# XMLを取得
response = requests.get(url)
response.encoding = "utf-8"

# XMLをパース
root = ET.fromstring(response.text)

# 名前空間の定義（Atomフィード特有）
ns = {"atom": "http://www.w3.org/2005/Atom"}

# 結果を入れるリスト
entries = []

# 各entry要素を抽出
for entry in root.findall("atom:entry", ns):
    title = entry.find("atom:title", ns).text
    updated = entry.find("atom:updated", ns).text
    author = entry.find("atom:author/atom:name", ns).text
    link = entry.find("atom:link", ns).attrib["href"]
    content = entry.find("atom:content", ns).text.strip() if entry.find("atom:content", ns) is not None else ""

    # 辞書としてまとめる
    entries.append({
        "title": title,
        "updated": updated,
        "author": author,
        "link": link,
        "content": content
    })

# JSON化
json_data = json.dumps(entries, ensure_ascii=False, indent=2)

# 出力例
print(json_data)
