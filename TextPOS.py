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
        relationship = set(['VB', 'VBD', 'VBN', 'VBP', 'VBZ', 'IN', 'CC']) #ADP is 'adposition'
	determiner = set(['WDT', 'DT', 'PDT'])
        names_list = [word[0] for word in tagged if (word[1] not in determiner and word[1] != '.' and word[1] not in relationship)]  #Discard determiners/connectors
        node_names = set(names_list)
	G = nx.Graph()
        print(names_list)
	print(tagged)
	for node in node_names: G.add_node(node)

        start_node = None
        start_sentence = True
        for word_i in tagged[1:]:
            if start_sentence:
                if word_i[0] in node_names:
                    start_node = word_i
                    start_sentence = False
                    continue
                else:
                    continue
            if word_i[1] in relationship or word_i[1] in determiner:
                continue
            if word_i[1] == '.':
                start_sentence = True
                continue
            G.add_edge(start_node[0], word_i[0])
            start_node  = word_i
        return G

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = TextBag("gita.txt", emb, word2id_dict, id2word_dict)
    bag.generate_graph()
