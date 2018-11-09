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
from TextBag import TextBag as GraphGenerator
from node2vec import Node2Vec

def gen_style_vec(graph, n_samples=100):
    '''
    Given StyleGraph, return a style vector
    '''
    n_nodes = nx.number_of_nodes(graph)
    if n_nodes < n_samples:
        n_samples = n_nodes

    #cf = nx.average_clustering(graph)
    random_sample = random.sample(graph.nodes(), n_samples)
    degree = np.mean([x[1] for x in graph.degree(random_sample)]) #nx.average_degree_connectivity(graph)
    #transitivity = nx.transitivity(graph)
    print("cluster began")
    avg_cluster = nx.average_clustering(graph, random_sample)
    print("cluster end")
    node2vec = Node2Vec(graph, workers=4, sampling_strategy='q')
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    average_vec = 0
    for node in graph.nodes():
        average_vec += model.wv.get_vector(node)
    average_vec /= n_nodes
    print(average)
    #print(list(nx.isolates(graph)), graph.nodes, graph.edges)
    #mxscc = max(nx.strongly_connected_components(graph), key=len)
    #mxwcc = max(nx.weakly_connected_components(graph), key=len)
    #shortest_path = nx.average_shortest_path_length(mxscc)

    #radius = nx.radius(mxwcc)
    #print(nx.is_connected(graph))
    #triads = nx.triadic_census(graph)
    #print(triads)
    return np.array([degree, avg_cluster] + average_vec)


if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = GraphGenerator("gita.txt", emb, word2id_dict, id2word_dict)
    G = bag.generate_graph()
    print(gen_style_vec(G))
