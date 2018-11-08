#!/usr/bin/env python

EMBEDDINGS = "./embeddings/glove.6B.300d.txt"
EMBEDDING_DIMS = (400000, 300)

def load_embeddings(reload_emb=False):
    emb_exists = os.path.isfile("./embeddings/emb.pickle")
    if reload_emb or not emb_exists:
        print("Loading embeddings from scratch - will take a moment")
        word2id_dict, id2word_dict = {}, {}
        embeddings = np.zeros(EMBEDDING_DIMS)
        with open(EMBEDDINGS) as open_emb:
            i = 0
            for line in open_emb:
                line = line.strip().split(' ')
                word2id_dict[line[0]] = i
                id2word_dict[i] = line[0]
                embeddings[i,:] = list(map(float, line[1:]))
                i += 1
            pickle.dump(open("./embeddings/emb.pickle", 'wb'), [embeddings, word2id_dict, id2word_dict])
    else:
        word2id_dict, id2word_dict, embeddings = pickle.load(open("./embeddings/emb.pickle", 'rb'))
    print("Embeddings loaded")
    return embeddings, word2id_dict, id2word_dict, embeddings
