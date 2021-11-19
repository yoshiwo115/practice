def word2vec(noun_word, component_array):
    from gensim.models import KeyedVectors
    # from gensim.models import Word2vec

    model = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)
    l = []

    for word in component_array:
        if word in model:
            if model.similarity(noun_word, word) < 0.4:
                l.append(word)
    print(l)
    return l

# component_array = ['風景', '桜', '顔', '遣り口']
# noun_word = '景色'

# l = word2vec(noun_word, component_array)

# proを選ぶとき用
from gensim.models import KeyedVectors

    model = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)
    l = []

    # 辞書の宣言
    dic = dict()

    jumanpp = Juman()    

    for word in all_propernoun_word_in_twitter:
        if word in model:
            result = jumanpp.analysis(word)
            for mrph in result.mrph_list(): # 各形態素にアクセス
                dic[word] = model.similarity(simile_noun_word, word)
    # 辞書のソート
    list = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    dic.clear()
    dic.update(list)
    print(dic)

    # keyだけ取り出す
    for key in dic.keys():
        l.append(key)

    # 最高のを抽出
    propernoun_word = l[0]