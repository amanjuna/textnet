"""
Graph_Generator.py

Template class specifying generic functions for GraphGenerator
Class

"""

import community
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class HyperGraph:
    def __init__(self, node_vectors, percentile_threshold):
        print("here")
        self.partition = {}
        embs = []
        node_names = []
        for item in node_vectors:
            node_names.append(item[0])
            embs.append(item[1])
        embs = np.array(embs)
        d = embs.dot(embs.T)
        l2 = (embs.T*embs.T).sum(0, keepdims=True)**0.5
        dist_matrix = d/l2/l2.T
        threshold = np.percentile(dist_matrix, percentile_threshold)
        print(threshold)
        G = nx.Graph()
        for name in node_names: G.add_node(name)
        for i, node_i in enumerate(node_names):
            for j in range(i+1, len(node_names)):
                node_j = node_names[j]
                if dist_matrix[i,j] > threshold:
                    G.add_edge(node_i, node_j, weight=dist_matrix[i,j])
        print("here")
        #print(G.nodes)
        G.remove_nodes_from(list(nx.isolates(G)))
        self.graph = G

    def get_num_nodes(self):
        return len(self.graph.nodes)

    def get_clusters(self):
        partition = community.best_partition(self.graph)
        return partition

    def gen_partitions_and_plot(self):
        self.partition = self.get_clusters()
        print(self.partition)
        pos = nx.spring_layout(self.graph)
        count = 0
        size = len(set(self.partition.values()))
        for com in set(self.partition.values()) :
            count = count + 1
            list_nodes = [nodes for nodes in self.partition.keys() if self.partition[nodes] == com]
            nx.draw_networkx_nodes(self.graph, pos, list_nodes, node_size = 20, node_color = str(float(count) / (size + 1)))
        nx.draw_networkx_edges(self.graph, pos)
        plt.show()

    def get_eigenvals(self):
        L = nx.normalized_graph_laplacian(self.graph)
        return np.linalg.eigvals(L)

if __name__=="__main__":
    vecs = []
    num_nodes = 20
    for i in range(num_nodes):
        vecs.append(('name' + str(i), np.random.random_sample((5, ))))
    #print(vecs)
    G = HyperGraph(vecs, 75)
    print('%d remaining nodes of %d' % (len(G.graph.nodes), num_nodes))
    #nx.draw(G.graph)
    #plt.show()
    G.gen_partitions_and_plot()
