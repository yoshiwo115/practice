import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

# xmlデータを一気に読み込む場合
# 重すぎてできなかった
# tree = ET.parse('kyoto-univ-web-cf-2.0.xml')
# 一番上の階層の要素取り出し
# root = tree.getroot()
# print(root.tag)
# print(root.attrib)


# メモリ開放しながら読む

context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))

_, entry = next(context)  # 一つ進めて root を得る

for event, elem in context:
    if event == 'end' and elem.tag == 'component':
        # do something on component
        print(elem.text)
        entry.clear()  # 用が済んだらrootを空に