from gensim.models import KeyedVectors

def word2vec(noun_word, component_array):
    for word in component_array:
        print(noun_word, word)
        print(model.similarity(noun_word, word))

model = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)
# model = gensim.models.Word2Vec.load('entity_vector.model.bin', binary=True)

# results = wv.most_similar(positive=['景色'])
# for result in results:
#     print(result)

print('読み込めてる')
component_array = ['風景', '桜', '顔']
noun_word = '景色'

word2vec(noun_word, component_array)