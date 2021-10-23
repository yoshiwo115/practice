import tweepy
import random
import re

# #Ginza
import spacy
from spacy import displacy
nlp = spacy.load('ja_ginza')
# #ここまで

f = open('twitter_token.txt', 'r')
datalist = [s.strip() for s in f.readlines()]
# ここに先程取得したAPIキーとトークンを入力
api_key = datalist[0]
api_secret_key = datalist[1]
access_token = datalist[2]
access_token_secret = datalist[3]

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

#インスタンス生成
api = tweepy.API(auth, wait_on_rate_limit=True)

# botのツイートを除外するため，一般的なクライアント名を列挙
sources = ["TweetDeck", "Twitter Web Client", "Twitter for iPhone",
            "Twitter for iPad", "Twitter for Android", "Twitter for Android Tablets",
            "ついっぷる", "Janetter", "twicca", "Keitai Web", "Twitter for Mac"]

#取得ツイート数
count = 50

#検索ワード
search_word = '綺麗だ 顔 -filter:retweets'

n=0
data=[]
#Ginza用のリスト
Ginzadata=[]

for result in tweepy.Cursor(api.search_tweets, q=search_word).items(count):
    n += 1
    print('----{}----'.format(n))
    print(result.text)
    data.append(result)
    Ginzadata.append(result.text)


# 最新ツイートの日時
data[0].created_at


print('\n')

# StGinzaリストを文字列に
StGinza = "".join(Ginzadata)

#Ginza
#ここでいろんな処理が行われる
doc = nlp(StGinza) 

for sent in doc.sents:
    for token in sent:
        print(token.i, token.orth_, token.lemma_, token.pos_, 
              token.tag_, token.dep_, token.head.i)

#固有表現抽出の結果の描画
# displacy.render(doc, style="ent")

# 抽出したエンティティの種類に対して色を指定する
colors = {"COUNTRY":"#00cc00", "CITY":"#00cc00", "GPE_OTHER":"#00cc00","OCCASION_OTHER":"#00cc00",
          "LOCATION":"#00cc00", "LOCATION_OTHER":"#00cc00","DOMESTIC_REGION":"#00cc00","PROVINCE":"#00cc00",
          "STATION":"#00cc00", "CONTINENTAL_REGION":"#00cc00","THEATER":"#00cc00",

          "TIME":"#adff2f","DATE":"#adff2f","DAY_OF_WEEK":"#adff2f",
          "PERIOD_YEAR":"#adff2f", "PERIOD_MONTH":"#adff2f", "PERIOD_DAY":"#adff2f",

          "FLORA":"#adff99","FLORA_PART":"#adff99",
          "DISH":"#ffeb99","FOOD_OTHER":"#ffeb99",

          "AGE":"#3385ff","N_PERSON":"#3385ff","N_EVENT":"#3385ff","N_LOCATION_OTHER":"#3385ff","RANK":"#3385ff",
          "N_PRODUCT":"#3385ff","":"#3385ff","":"#3385ff","":"#3385ff","MEASUREMENT_OTHER":"#3385ff","PERCENT":"#3385ff",
          "N_ORGANIZATION":"#3385ff", "ORDINAL_NUMBER":"#3385ff", "N_FACILITY":"#3385ff","SPEED":"#3385ff",
          "PHONE_NUMBER":"#3385ff",

          "MONEY":"#ffff00",

          "COMPANY":"#99c2ff", "SCHOOL":"#99c2ff", "INTERNATIONAL_ORGANIZATION":"#99c2ff",
          "GOE_OTHER":"#99c2ff", "SHOW_ORGANIZATION":"#99c2ff","CORPORATION_OTHER":"#99c2ff",

          "CLOTHING":"#ff66a3",
          "PRODUCT_OTHER":"#ff66a3",

          "PERSON":"#c266ff",
          "POSITION_VOCATION":"#ebccff",

          "MUSIC":"#ff7f50", "MOVIE":"#ff7f50", "GAME":"#ff7f50", "SPORT":"#ff7f50", "BOOK":"#ff7f50", 
          "BROADCAST_PROGRAM":"#ff7f50", 

          "ANIMAL_DISEASE":"#cd5c5c"
          }

options = {"colors": colors}
displacy.serve(doc, style="ent", options=options)
#ここまで





# --------------------------------------------------------------------------
# VRアカデミアのやつ

# import requests 
# import os 
# import urllib 
# import json 
# bearer_token = os.environ.get("BEARER_TOKEN") 

# headers = {"Authorization": f"Bearer {bearer_token}"} 
# vr_academia = urllib.parse.quote('#VRアカデミア') 
# url = f'https://api.twitter.com/2/tweets/search/recent?query={vr_academia} -is:retweet'
# response =  requests.get(url, headers=headers) 
# json_response = response.json()

# print(json.dumps(json_response, indent=2, ensure_ascii=False)) 