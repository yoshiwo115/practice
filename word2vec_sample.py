from gensim.models import KeyedVectors

wv = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)
results = wv.most_similar(negative=['景色'])
for result in results:
    print(result)