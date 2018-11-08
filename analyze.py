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
- what else?
'''
import networkx as nx
import numpy as np
from utils import *
from TextBag import TextBag as GraphGenerator


def gen_style_vec(graph):
    '''
    Given StyleGraph, return a style vector
    '''
    #cf = nx.average_clustering(graph)
    degree = np.mean([x[1] for x in graph.degree(graph.nodes())])#nx.average_degree_connectivity(graph)
    transitivity = nx.transitivity(graph)
    avg_cluster = nx.average_clustering(graph)
    #print(list(nx.isolates(graph)), graph.nodes, graph.edges)
    #mxscc = max(nx.strongly_connected_components(graph), key=len)
    #mxwcc = max(nx.weakly_connected_components(graph), key=len)
    #shortest_path = nx.average_shortest_path_length(mxscc)

    #radius = nx.radius(mxwcc)
    #print(nx.is_connected(graph))
    #triads = nx.triadic_census(graph)
    #print(triads)
    return np.array([degree, transitivity, avg_cluster])


if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    bag = GraphGenerator("gita.txt", emb, word2id_dict, id2word_dict)
    G = bag.generate_graph()
    print(gen_style_vec(G))
