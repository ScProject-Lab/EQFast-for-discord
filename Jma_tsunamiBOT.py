import xml.etree.ElementTree as ET
import requests

with open("2024ishikawa.xml", "r", encoding="utf-8") as f:
    xml_str = f.read()

root = ET.fromstring(xml_str)
print(root)

ns = {
    'jmx': 'http://xml.kishou.go.jp/jmaxml1/',
    'seis': 'http://xml.kishou.go.jp/jmaxml1/body/seismology1/',
    'eb': 'http://xml.kishou.go.jp/jmaxml1/elementBasis1/',
}

area = []
level = []
headline = ""

for Body in root.findall('seis:Body', ns):
    for item in Body.findall('.//seis:Item', ns):
        area.append(item.find('.//seis:Area/seis:Name', ns).text)
    for kind in Body.findall('.//seis:Kind/seis:Name', ns):
        level.append(kind.text)

warning_dict = {}

for i in range(len(level)):
    lv = level[i]
    ar = area[i]

    if lv not in warning_dict:
        warning_dict[lv] = []

    warning_dict[lv].append(ar)

s_str = ""

for lv, areas in warning_dict.items():
    s_str += f"{lv}\n"
    for a in areas:
        s_str += f"  {a}\n"

print(s_str)
