#!/usr/bin/env python

#from StyleGraph import StyleGraph
from GraphGenerator import GraphGenerator
from utils import *
import networkx as nx
import numpy as np
import scipy.spatial as ss

class TextWindow(GraphGenerator):
    def generate_graph(self):
        node_names = list(set(self.tokens))
        if "UNK" in node_names: node_names.remove("UNK")
        node_ids = np.array([self.word2id(name) for name in node_names])
        G = nx.Graph()
        for node in node_names: G.add_node(node)

        for i in range(len(self.tokens) - 1)
            start = self.tokens[i]
            end = self.tokens[i + 1]
            if start == '.' or end == '.': continue
            G.add_edge(start, end)
        return G

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    window = TextWindow("gita.txt", emb, word2id_dict, id2word_dict)
    G = window.generate_graph()
