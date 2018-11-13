'''
analyze.py

Analyzes a given StyleGraph object, writes the analysis to file,
and returns a style vector

Things in the style vector:
- the motif vector
- avg clustering coefficient
- avg graph width
- rolX vector
- avg degree
- what else
'''
import networkx as nx
import numpy as np
import random
from utils import *
from node2vec import Node2Vec
from TextPOSDirected import TextPOSDirected as GraphGenerator
import matplotlib.pyplot as plt
def gen_style_vec(graph, n_samples=100):
    '''
    Given StyleGraph, return a style vector
    '''
    n_nodes = nx.number_of_nodes(graph)
    if n_nodes < n_samples:
        n_samples = n_nodes
    nx.draw_networkx(graph, with_labels=False)
    plt.savefig("okay5.png")
	  #cf = nx.average_clustering(graph)
    random_sample = random.sample(graph.nodes(), n_samples)
    degree = np.mean([x[1] for x in graph.degree(random_sample)]) #nx.average_degree_connectivity(graph)
    #transitivity = nx.transitivity(graph)
    print("cluster began")
    avg_cluster = nx.average_clustering(graph, random_sample)
    print("cluster end")

    #triads = nx.triadic_census(graph)
    #triads = [(key, value) for key, value in triads.items()]
    #triads.sort(key=lambda x: x[0])
    #triads = [x[1] for x in triads]
    #graph = graph.to_undirected()
    graph = create_analysis_node(graph)
    node2vec = Node2Vec(graph, workers=4)
    model = node2vec.fit()
    #average_vec = 0
    #for node in graph.nodes():
    #    average_vec += model.wv.get_vector(node)
    #average_vec /= n_nodes
    #print(average_vec)
    #print(list(nx.isolates(graph)), graph.nodes, graph.edges)
    #mxscc = max(nx.strongly_connected_components(graph), key=len)
    #mxwcc = max(nx.weakly_connected_components(graph), key=len)
    #shortest_path = nx.average_shortest_path_length(mxscc)
    analysis_vec = model.wv.get_vector('ANALYSIS_NODE')
    #print(np.array([degree, avg_cluster] + triads))
    #radius = nx.radius(mxwcc)
    #print(nx.is_connected(graph))
    #triads = nx.triadic_census(graph)
    #print(triads)

    return np.concatenate((np.array([degree, avg_cluster]), analysis_vec))

def create_analysis_node(G):
    G.add_node("ANALYSIS_NODE")
    for n in G.nodes:
        G.add_edge("ANALYSIS_NODE", n)
    return G


if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = GraphGenerator("test.txt", emb, word2id_dict, id2word_dict)
    G = bag.generate_graph()
    print(gen_style_vec(G))
