# User入力機構
def user_input():
    input_dialogue = input()
    return input_dialogue

# 文情報解析機構
def sentence_analysys(sentence):
    # pyKNPで格情報取得
    return 0

from pyknp import KNP

knp = KNP()

result = knp.parse(user_input())

for tag in result.tag_list():
    if tag.pas is not None: # find predicate
        print('述語: %s' % ''.join(mrph.midasi for mrph in tag.mrph_list()))
        for case, args in tag.pas.arguments.items(): # case: str, args: list of Argument class
            for arg in args: # arg: Argument class
                print('\t格: %s,  項: %s  (項の基本句ID: %d)' % (case, arg.midasi, arg.tid))