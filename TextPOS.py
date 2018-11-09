#!/usr/bin/env python

from GraphGenerator import GraphGenerator
from utils import *
import nltk
import networkx as nx
import numpy as np
import scipy.spatial as ss

class TextPOS(GraphGenerator):
    def generate_graph(self):
        tagged = nltk.pos_tag(self.tokens)
        relationship = set(['VERB', 'CONJ', 'ADP']) #ADP is 'adposition'
        node_names = set([word[0] for word in tagged if (word[1] != 'DET' and word[1] != '.' and word[1] not in relationship)]) #Discard determiners/connectors
        G = nx.Graph()
        for node in node_names: G.add_node(node)

        start_node = tagged[0]
        start_sentence = False
        for i, word_i in enumerate(tagged):
            if start_sentence:
                if word_i[1] not in relationship and word_i[1] != 'DET' and word_i[1] != '.':
                    start_node = word_i
                    start_sentence = False
                    continue
                else:
                    continue
            if word_i[1] in relationship or word_i[1] == 'DET':
                continue
            if word_i[1] == '.':
                start_sentence = True
                continue
            G.add_edge(start_node[0], word_i[0])
	return G


if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = TextPOS("gita.txt", emb, word2id_dict, id2word_dict)
    bag.generate_graph()
