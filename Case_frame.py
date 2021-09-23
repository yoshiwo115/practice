import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

# メモリ開放しながら読む

context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))

#next関数_イテレータを回して、読んだ要素は消す
# >>>iter_a = [1,2,3,4,5]
# >>>print(next(iter_a))
# 1
# >>>print(next(iter_a))
# 2
_, entry = next(context)  # 一つ進めてentryを得る
print(entry)

#<entry headword="あいにくだ/あいにくだ" predtype="形">
# headword="あいにくだ/あいにくだ" ここをxmlで扱うには

for event, elem in context:
    print(event)
    if event == 'end' and elem.tag == 'component': # </component>が来たら
        # do something on component
        print(elem.text)
        break
        entry.clear()  # entryを空にしてメモリ開放