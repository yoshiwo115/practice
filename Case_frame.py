import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

#xmlデータを読み込みます
tree = ET.parse('../../kyoto-univ-web-cf-2.0/kyoto-univ-web-cf-2.0.xml')
#一番上の階層の要素を取り出します
root = tree.getroot()

print(root.tag)
print(root.attrib)