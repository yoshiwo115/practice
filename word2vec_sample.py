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