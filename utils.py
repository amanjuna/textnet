#!/usr/bin/env python

EMBEDDINGS = "./embeddings/glove.6B.300d.txt"
EMBEDDING_DIMS = (400000, 300)

def load_embeddings(self):
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
    return word2id_dict, id2word_dict, embeddings
