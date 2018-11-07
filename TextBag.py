#!/usr/bin/env python

from Graph_Generator import GraphGenerator
import networkx as nx
import numpy as np
import scipy.spatial as ss

PERCENTILE_THRESHOLD = 75

class TextBag(GraphGenerator):
    def generate_graph(self):
        node_names = list(set(self.tokens))
        node_ids = np.array([self.word2id(name) for name in node_names])
        embs = self.emb[node_ids,:]
        print(embs.shape)
        d = embs.dot(embs.T)
        l2 = (embs.T*embs.T).sum(0, keepdims=True)**0.5
        dist_matrix = d/l2/l2.T
        threshold = np.percentile(dist_matrix, PERCENTILE_THRESHOLD)
        G = nx.Graph()
        for node in node_names: G.add_node(node)
        for i, node_i in enumerate(node_names):
            for j in range(i+1, len(node_names)):
                node_j = node_names[j]
                if dist_matrix[i,j] > threshold:
                    G.add_edge(node_i, node_j, weight=dist_matrix[i,j])


if __name__=="__main__":
    bag = TextBag("gita.txt")
    bag.generate_graph()
