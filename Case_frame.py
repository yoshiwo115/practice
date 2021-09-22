import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

#xmlデータを読み込み
tree = ET.parse('kyoto-univ-web-cf-2.0.xml')
#一番上の階層の要素取り出し
root = tree.getroot()

print(root.tag)
print(root.attrib)