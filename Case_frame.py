# 格フレームを読むファイル

import random
import re

# 検索ワード
noun_word = "景色"
declinable_word = "綺麗"

import xml.etree.ElementTree as ET

# メモリ開放しながらxmlを読む

context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))

for event,elem in context:
    if event == 'start' and elem.tag == 'entry' and 'あえない' in elem.attrib['headword']: 
        # headwordが特定の用言だったとき
            
            print(elem.attrib) #何で検索されているか表示
            
            for event, elem in context: 
                #entry以下でループを回す
                
                if event == 'end' and elem.tag == 'entry': 
                    #entryのendタグが来たら
                    
                    break #ループを抜ける

                elif event == 'end' and elem.tag == 'component': 
                    #componentのendタグか来たら
                    
                    print(elem.text) #内容を表示
    else:
        elem.clear()
        # メモリを開放する