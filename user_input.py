# User入力機構
def user_input():
    return input()

# 文情報解析機構
def sentence_analysys(sentence):
    # pyKNPで格情報取得
    knp = KNP()
    result = knp.parse(sentence)
    noun_word = ''
    declinable_word = ''
    case = ''

    for tag in result.tag_list():
        if tag.pas is not None: # find predicate
            declinable_word = ''.join(mrph.midasi for mrph in tag.mrph_list())
            print('述語: '+ declinable_word)
            for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
                for arg in args: # arg: Argument class
                    print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))
                    noun_word = arg.midasi
                    case = case

    return noun_word, declinable_word, case

# 直喩名詞選択機構
def select_simile_noun_word(noun_word, declinable_word, case):
    import random
    simile_noun_word = random.choice(search_caseframe(declinable_word))
    print('slimile_' + simile_noun_word)

    return simile_noun_word

# 格フレーム検索
def search_caseframe(declinable_word):
    import xml.etree.ElementTree as ET

    component_array = []

    context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))
    # メモリ開放しながらxmlを読む
    for event,elem in context:
        if event == 'start' and elem.tag == 'entry' and declinable_word in elem.attrib['headword']: 
            # headwordに特定の用言が含まれていたとき
                
                for event, elem in context: 
                    #entry以下でループを回す
                    
                    if event == 'end' and elem.tag == 'entry': 
                        #entryのendタグが来たら 
                        print(elem.attrib) #何で検索されているか表示
                        elem.clear()
                        return component_array #ループを抜ける

                    elif event == 'end' and elem.tag == 'component': 
                        #componentのendタグか来たら
                        
                        # print(elem.text) #内容を表示
                        print(elem.text)
                        component_array.append(elem.text)
        else:
            elem.clear()
            # メモリを開放する
    
    return "なんもなし"

# 固有名詞選択機構
def select_propernoun():
    return 0

# twitter検索
def search_twitter():
    return 0

# 出力
def system_output():
    return 0



from pyknp import KNP

# user入力文
input_dialogue = user_input()

# 文情報解析結果
result = sentence_analysys(input_dialogue)

# 名詞
noun_word = result[0]
# 用言
declinable_word = result[1]
# 格
case = result[2]

# 直喩に使う名詞
simile_noun_word = select_simile_noun_word(noun_word, declinable_word, case)
