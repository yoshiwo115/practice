from pyknp import KNP
from pyknp import Juman
import random
import re
import time

# 文情報解析機構
def sentence_analysys(sentence):
    # pyKNPで格情報取得
    knp = KNP()
    result = knp.parse(sentence)

    noun_word = ''
    declinable_word = ''
    case = ''

    for tag in result.tag_list():
        if tag.pas is not None: # 述語を見つける
            declinable_word = tag.repname # 正規化代表表記を保存
            for case, args in tag.pas.arguments.items(): # case: 格, args: Argumentのリスト https://pyknp.readthedocs.io/en/latest/tag.html#pyknp.knp.pas.Pas.arguments
                for arg in args:
                    noun_word = arg.midasi
                    case = case

    return noun_word, declinable_word, case

# 直喩名詞選択機構
def select_simile_noun_word(noun_word, declinable_word, case):
    
    component_array = search_caseframe(declinable_word, case)

    # 綺麗にした後の
    component_array_after = []
    
    # /以降の文字削除
    for word in component_array:
        # twitter検索用に直喩名詞の/以下を削除
        #<>とか削除
        component_array_after.append(re.sub('[<>]', '', word.split('/')[0]))
    
    # word2vecにかける
    l = word2vec(noun_word, component_array_after)

    simile_noun_word = random.choice(l)

    if simile_noun_word == "×":
        print('村上春樹くらい分からない')

    return simile_noun_word

# 格フレーム検索xmltree
# def search_caseframe(declinable_word, case):
    import xml.etree.ElementTree as ET

    component_array = []

    context = ET.iterparse('kyoto-univ-web-cf-2.0.xml', events=('start', 'end'))
    # メモリ開放しながらxmlを読む
    for event,elem in context:
        if event == 'start' and elem.tag == 'entry' and declinable_word == elem.attrib['headword']: 
            # headwordに特定の用言が含まれていたとき
                
                for event, elem in context: 
                    #entry以下でループを回す
                    
                    if event == 'end' and elem.tag == 'entry': 
                        # entryのendタグが来たら 
                        # print(elem.attrib) #何で検索されているか表示
                        elem.clear()
                        return component_array #ループを抜ける

                    if event == 'start' and elem.tag == 'argument' and case in elem.attrib['case']:

                        for event, elem in context:
                            #argument以下でループを回す
                            
                            if event == 'end' and elem.tag == 'argument':
                                elem.clear()
                                break # ループを抜けて次のargumentを読む

                            elif event == 'end' and elem.tag == 'component':
                                component_array.append(elem.text)
                                # print(elem.text)
                    else:
                        elem.clear()
                        # argumentタグ以下のメモリを開放する⇒次のargumentを読む
        else:
            elem.clear()
            # entryタグ以下のメモリを開放する⇒次のentryを読む
    
    return "×"

# 格フレーム検索baseX
def search_caseframe(declinable_word, case):
    from BaseXClient import BaseXClient

    component_array = []

    # セッション作成
    session = BaseXClient.Session('test-host', 1984, 'admin', 'admin')

    try:
        # DBオープン
        session.execute("open case")
        print(session.info())

        # DBの内容を表示 & 形式整え
        a = session.execute(f"xquery //entry[@headword='{declinable_word}']/caseframe/argument[contains(@case,'{case}')]/component")
        aa = a.replace('</component>', '')
        aaa = re.sub(r"[a-z]", '', aa)
        aaaa = re.sub(r"[0-9]", '', aaa)
        aaaaa = aaaa.replace("< =\"\">", '')
        # print(aaaaa)

        component_array = aaaaa.split("\n")
        print("正常終了しました\n")

    finally:
        # セッションを閉じる
        if session:
            session.close()
    
    return component_array

# 単語距離測定
def word2vec(noun_word, component_array):
    from gensim.models import KeyedVectors

    model = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)
    l = []

    # 辞書の宣言
    dic = dict()

    jumanpp = Juman()    

    for word in component_array:
        if word in model:
            result = jumanpp.analysis(word)
            for mrph in result.mrph_list(): # 各形態素にアクセス
                if mrph.bunrui == '普通名詞':
                    dic[word] = model.similarity(noun_word, word)

    # 辞書のソート
    list = sorted(dic.items(), key=lambda x:x[1])
    dic.clear()
    dic.update(list)
    print(dic)

    # keyだけ取り出す
    for key in dic.keys():
        l.append(key)

    # 上からいくつかを抽出
    num = round((len(l)/2))
    l2 = l[:num]

    return l2

# twitter検索
def search_twitter(declinable_word, simile_noun_word, result_type):
    import tweepy

    f = open('twitter_token.txt', 'r')
    datalist = [s.strip() for s in f.readlines()]
    api_key = datalist[0]
    api_secret_key = datalist[1]
    access_token = datalist[2]
    access_token_secret = datalist[3]

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    # インスタンス生成
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # botのツイートを除外するため，一般的なクライアント名を列挙
    sources = ["TweetDeck", "Twitter Web Client", "Twitter for iPhone",
                "Twitter for iPad", "Twitter for Android", "Twitter for Android Tablets",
                "ついっぷる", "Janetter", "twicca", "Keitai Web", "Twitter for Mac"]

    # 取得ツイート数
    count = 50
    # カウント変数
    n = 0
    # 空のリスト
    results_text_list = []

    #検索ワード
    search_word = declinable_word + " " + simile_noun_word + " " + '-filter:retweets -filter:replies -filter:quote'
    print('・twitter検索ワード: ' + search_word + '\n')

    # APIの場合
    tweets = api.search_tweets(q=search_word, lang='ja', result_type=result_type, count=count)
    for s in tweets:
        if s.source in sources and "http" not in s.text and "#" not in s.text:
            n += 1
            print('----{}----'.format(n))
            print(s.text) 
            results_text_list.append(str(s.text).replace(" ", "").replace('　', ''))

    # results_text_listリストを文字列に
    search_twitter_results = "".join(results_text_list).replace(" ", "")
    
    # 何も取得できていなかったら
    if search_twitter_results == "":
        search_twitter_results == "無取得男"

    return search_twitter_results

# 固有名詞選択機構
def select_propernoun(simile_noun_word, search_twitter_results):
    # 用言と項構造になっている固有名詞を抽出
    
    jumanpp = Juman()
    juman_result = jumanpp.analysis(search_twitter_results)

    
    # KNPも追加したいがうまくいかない
    # knp = KNP()
    # knp_result = knp.parse(search_twitter_results)

    all_propernoun_word_in_twitter = []

    for mrph in juman_result.mrph_list(): # 各形態素にアクセス
        if mrph.bunrui == '人名' or mrph.bunrui == '地名' or mrph.bunrui == '組織名' or mrph.bunrui == '固有名詞':
            print(mrph.midasi)
            all_propernoun_word_in_twitter.append(mrph.midasi)

    if all_propernoun_word_in_twitter == []:
        # 何も取得できなかった場合
        all_propernoun_word_in_twitter = ['吉田ジャネット']

    propernoun_word = random.choice(all_propernoun_word_in_twitter)
    
    

    return propernoun_word

def main():

    shinkisei_flag = True
    igaisei_flag = True
    gutaisei_flag = True

    # User入力
    input_dialogue = input('・User入力: ')
    # 処理前の時刻
    t1 = time.time()
    # 文情報解析結果
    print('・文情報解析')
    sentence_analysys_result = sentence_analysys(input_dialogue)
    t2 = time.time()
    # 名詞, 用言, 格
    noun_word, declinable_word, case = sentence_analysys_result
    print(noun_word, declinable_word, case)

    if igaisei_flag == True:
        # 直喩に使う名詞
        simile_noun_word = select_simile_noun_word(noun_word, declinable_word, case)
    else:
        simile_noun_word = noun_word
    
    print('・直喩名詞: ' + simile_noun_word)
    # 処理後の時刻
    t3 = time.time()
    # twitter検索用に用言の/以下を削除
    declinable_word = declinable_word.split('/')[0]

    if shinkisei_flag == True:
        # twitter検索
        search_twitter_results = search_twitter(declinable_word, simile_noun_word, 'recent')
    else:
        search_twitter_results = search_twitter(declinable_word, simile_noun_word, 'popular')
    
    # 処理後の時刻
    t4 = time.time()

    if gutaisei_flag == True:
        # 固有名詞選択
        propernoun_word = select_propernoun(simile_noun_word, search_twitter_results)
    else:
        propernoun_word = ''

    print('選択した固有名詞: ' + propernoun_word)

    # 処理後の時刻
    t5 = time.time()

    # 合体
    if gutaisei_flag == True:
        propernoun_word = propernoun_word + 'の'

    result = 'そうだね。' + propernoun_word + simile_noun_word + 'くらい' + declinable_word + 'ね'
    
    # 出力
    print('・system出力: ' + result)

    # 経過時間を表示
    time1 = t2-t1
    time2 = t3-t2
    time3 = t4-t3
    time4 = t5-t4
    print(f"文解析時間：{time1}")
    print(f"直喩名詞選択時間：{time2}")
    print(f"twitter検索時間：{time3}")
    print(f"固有名詞選択時間：{time4}")

if __name__ == "__main__":
    main()
