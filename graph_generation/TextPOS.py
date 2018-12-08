#!/usr/bin/env python

from graph_generation.GraphGenerator import GraphGenerator
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
        punctuation = set([',', '(', ')', '``', "''", ',', '<', '>'])
        names_list = [word for word in tagged if (word[1] not in determiner and word[1] != '.' and word[1] not in relationship
                                                  and word[0] != 'UNK' and word[0] not in punctuation)]  #Discard determiners/connectors
        node_names = set(names_list)
        G = nx.Graph()
        for node in node_names: G.add_node(node)
        start_node = None
        start_sentence = True

        for word_i in names_list:
            if start_sentence:
                if word_i in node_names:
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
            G.add_edge(start_node, word_i)
            start_node  = word_i
        return G

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    pos = TextPOS("gita.txt", emb, word2id_dict, id2word_dict)
    pos.generate_graph()
