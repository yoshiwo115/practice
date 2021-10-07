# 公式Docs
from __future__ import unicode_literals # It is not necessary when you use python3.
# from pyknp import Juman
# jumanpp = Juman() 
# # default is JUMAN++: Juman(jumanpp=True). if you use JUMAN, use Juman(jumanpp=False)
# result = jumanpp.analysis("下鴨神社の参道は暗かった。")
# for mrph in result.mrph_list(): # 各形態素にアクセス
#     print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
#             % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

# yusanishのやつ
import pyknp
knp = pyknp.KNP()
knp = pyknp.KNP(jumanpp=True)
result = knp.parse("この景色綺麗だね。")
result.draw_bnst_tree()