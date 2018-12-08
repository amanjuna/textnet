#!/usr/bin/env python

#from StyleGraph import StyleGraph
from GraphGenerator import GraphGenerator
from utils import *
import networkx as nx
import numpy as np
import scipy.spatial as ss
import itertools

class TextSharedSentence(GraphGenerator):
    def generate_graph(self):
        node_names = list(set(self.tokens))
        if "UNK" in node_names: node_names.remove("UNK")
        G = nx.Graph()
        for node in node_names: G.add_node(node)
        sentences = np.split(self.tokens, np.where(self.tokens = '.'))

        for s in sentences:
            pairs = itertools.combinations(s)
            G.add_edges_from(pairs)

        return G

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = TextBag("gita.txt", emb, word2id_dict, id2word_dict)
    G = bag.generate_graph()
