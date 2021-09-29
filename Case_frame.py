# 格フレームを読むファイル

import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

# メモリ開放しながら読みたい

context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))

for event,elem in context:
    if event == 'start' and elem.tag == 'entry' and 'あえない' in elem.attrib['headword']:
            print(elem.attrib)

            for event, elem in context:
                if event == 'end' and elem.tag == 'entry':
                    break
                elif event == 'end' and elem.tag == 'component':
                    print(elem.text)
    else:
        elem.clear()