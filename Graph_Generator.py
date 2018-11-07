"""
Graph_Generator.py

Template class specifying generic functions for GraphGenerator
Class

"""

import numpy as np
import os, pickle, nltk

EMBEDDINGS = "./embeddings/glove.6B.300d.txt"
EMBEDDING_DIMS = (400000, 300)

class GraphGenerator:
    def __init__(self, txt_file, load_emb=False):
        emb_exists = os.path.isfile("./embeddings/emb.pickle")
        if load_emb or not emb_exists:
            print("Loading embeddings from scratch - will take a moment")
            emb_data = self.load_embeddings()
            pickle.dump(emb_data, open("./embeddings/emb.pickle", 'wb'))
        emb_data = pickle.load(open("./embeddings/emb.pickle", 'rb'))
        print("Embeddings loaded")
        self.word2id_dict, self.id2word_dict, self.emb = emb_data
        self.tokens = self.tokenize(txt_file)

    def generate_graph(self):
        print("Needs to be called on a child of the GraphGenerator Class")
        pass

    def tokenize(self, txt_file):
        tokens = []
        with open(txt_file, 'r') as open_doc:
            for line in open_doc:
                for token in nltk.word_tokenize(line):
                    lower = token.lower()
                    if lower in self.word2id_dict:
                        tokens += [lower]
        return tokens

    def word2id(self, word):
        return self.word2id_dict[word]

    def id2word(self, id):
        return self.id2word_dict[id]

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

if __name__=="__main__":
    gg = GraphGenerator("gita.txt")
    #gg.load_embeddings()
