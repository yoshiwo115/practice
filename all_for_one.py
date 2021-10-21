from pyknp import KNP
from pyknp import Juman
import random


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
            declinable_word = tag.repname
            # print('述語: '+ declinable_word)
            for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
                # print(get_arguments(case))
                for arg in args: # arg: Argument class
                    noun_word = arg.midasi
                    case = case

    return noun_word, declinable_word, case

# 直喩名詞選択機構
def select_simile_noun_word(noun_word, declinable_word, case):
    
    simile_noun_word = random.choice(search_caseframe(declinable_word, case))

    if simile_noun_word == "×":
        print('村上春樹くらい分からない')

    # /以降の文字削除
    simile_noun_word = simile_noun_word.split('/')[0]

    return simile_noun_word

# 格フレーム検索
def search_caseframe(declinable_word, case):
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

# twitter検索
def search_twitter(declinable_word, simile_noun_word):
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
    count = 5

    # カウント変数
    n = 0

    # 空のリスト
    results_text_list = []

    #検索ワード
    search_word = declinable_word + " " + simile_noun_word + " " + '-filter:retweets -filter:replies'
    print(search_word)

    # search_results = api.search_tweets(q = search_word, count = count)
    for result in tweepy.Cursor(api.search_tweets, q=search_word).items(count):
    # for result in search_results:
        # print(result.text)
        results_text_list.append(result.text)

    # results_text_listリストを文字列に
    search_twitter_results = "".join(results_text_list)
    search_twitter_results = search_twitter_results.replace(" ", "")
    search_twitter_results = str(search_twitter_results)
    
    if search_twitter_results == "":
        search_twitter_results = "森田さん空です"

    return search_twitter_results

# 固有名詞選択機構
def select_propernoun(search_twitter_results):
    # 用言と項構造になっている固有名詞を抽出
    
    jumanpp = Juman()
    all_propernoun_word_in_twitter = []
    
    result = jumanpp.analysis(search_twitter_results)

    for mrph in result.mrph_list(): # 各形態素にアクセス
        if mrph.bunrui == '固有名詞' or mrph.bunrui == '人名' or mrph.bunrui == '地名' or mrph.bunrui == '組織名':
            all_propernoun_word_in_twitter.append(mrph.midasi)

    if all_propernoun_word_in_twitter == []:
        all_propernoun_word_in_twitter = ['固有名詞なし']

    propernoun_word = random.choice(all_propernoun_word_in_twitter)

    return propernoun_word


def main():

    # User入力
    input_dialogue = input('User入力: ')

    # 文情報解析結果
    sentence_analysys_result = sentence_analysys(input_dialogue)

    # 名詞
    noun_word = sentence_analysys_result[0]
    # 用言
    declinable_word = sentence_analysys_result[1]
    # 格
    case = sentence_analysys_result[2] + '格'

    # 直喩に使う名詞
    simile_noun_word = select_simile_noun_word(noun_word, declinable_word, case)
    
    # twitter検索用に/以下を削除
    declinable_word = declinable_word.split('/')[0]

    # twitter検索
    search_twitter_results = search_twitter(declinable_word, simile_noun_word)

    # 固有名詞選択
    propernoun_word = select_propernoun(search_twitter_results)

    # 合体
    result = 'そうだね。' + propernoun_word + 'の' + simile_noun_word + 'くらい' + declinable_word + 'ね'
    
    # 出力
    print(result)

if __name__ == "__main__":
    main()