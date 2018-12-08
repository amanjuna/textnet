#!/usr/bin/env python

import os, pickle
import numpy as np

EMBEDDINGS = "../embeddings/glove.6B.300d.txt"
EMBEDDING_DIMS = (400001, 300)

def load_embeddings(reload_emb=False):
    emb_exists = os.path.isfile("../embeddings/emb.pickle")
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
            embeddings[EMBEDDING_DIMS[0] - 1,:] = [float('inf') for i in range(EMBEDDING_DIMS[1])]
            word2id_dict["UNK"] = EMBEDDING_DIMS[0] - 1
            id2word_dict[EMBEDDING_DIMS[0] - 1] = "UNK"

            pickle.dump([embeddings, word2id_dict, id2word_dict], open("../embeddings/emb.pickle", 'wb'))
    else:
        embeddings, word2id_dict, id2word_dict = pickle.load(open("../embeddings/emb.pickle", 'rb'))
    print("Embeddings loaded")
    return embeddings, word2id_dict, id2word_dict
