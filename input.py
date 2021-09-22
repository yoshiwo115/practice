#Ginza準備
import spacy
from spacy import displacy
nlp = spacy.load('ja_ginza')
#ここまで

#形態素解析

#ユーザー入力
input_dialogue = input()
#Ginzaに通す
doc = nlp(input_dialogue)

#名詞保存変数グローバル宣言
noun_word = ""
#用言保存変数グローバル宣言
declinable_word = ""

for sent in doc.sents:
    for token in sent:
        if token.pos_=="NOUN":
            noun_word = token.orth_ #名詞抜き出し
        elif token.pos_=="ADJ" or token.pos_=="VERB":
            declinable_word = token.orth_ #用言抜き出し

print("search_word:", noun_word, declinable_word)