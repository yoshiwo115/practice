# search_word決定機構

# Ginza準備
import spacy
from spacy import displacy
nlp = spacy.load('ja_ginza')

# ユーザー入力
input_dialogue = input()

# 形態素解析------------------------------------------------------------
# Ginzaに通す
doc = nlp(input_dialogue)

# 名詞保存変数グローバル宣言
noun_word = ""
# 用言保存変数グローバル宣言
declinable_word = ""

for sent in doc.sents:
    for token in sent:
        if token.pos_=="NOUN":
            # 名詞抜き出し
            noun_word = token.orth_ 
        elif token.pos_=="ADJ" or token.pos_=="VERB":
            # 用言抜き出し
            declinable_word = token.orth_

print("search_word:", noun_word, declinable_word)