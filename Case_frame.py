# 格フレームを読むファイル

import random
import re

# 検索ワード
input_noun_word = "景色"
input_declinable_word = "綺麗"

import xml.etree.ElementTree as ET

def search_noun():
    context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))
    # メモリ開放しながらxmlを読む
    for event,elem in context:
        if event == 'start' and elem.tag == 'entry' and input_declinable_word in elem.attrib['headword']: 
            # headwordに特定の用言が含まれていたとき
                
                print(elem.attrib) #何で検索されているか表示
                
                for event, elem in context: 
                    #entry以下でループを回す
                    
                    if event == 'end' and elem.tag == 'entry': 
                        #entryのendタグが来たら 
                        
                        elem.clear()
                        return 0 #ループを抜ける

                    elif event == 'end' and elem.tag == 'component': 
                        #componentのendタグか来たら
                        
                        print(elem.text) #内容を表示
        else:
            elem.clear()
            # メモリを開放する


search_noun()

print('\n終わり')