# User入力機構
def user_input():
    input_dialogue = input()
    return input_dialogue

# 文情報解析機構
def sentence_analysys(sentence):
    # pyKNPで格情報取得
    return 0

import re
import pyknp 

knp = pyknp.KNP(jumanpp=True)
result = knp.parse("この景色綺麗だね。")