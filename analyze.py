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
from graph_generation.TextPOS import TextPOS as GraphGenerator
import matplotlib.pyplot as plt

def gen_style_vec(graph, word2id_dict, emb, n_samples=100):
    '''
    Given StyleGraph, return a style vector
    '''
    # Graph stats
    n_nodes = nx.number_of_nodes(graph)
    if n_nodes < n_samples:
        n_samples = n_nodes
    nx.draw_networkx(graph, with_labels=False)
    random_sample = random.sample(graph.nodes(), n_samples)
    avg_degree = np.mean([x[1] for x in graph.degree(random_sample)])
    avg_cluster = nx.average_clustering(graph, random_sample)
    graph_stats = np.array([avg_degree, avg_cluster])

    # Centrality
    centrality = nx.eigenvector_centrality_numpy(graph)
    sorted_centrality = sorted(centrality.items(), key=lambda x:x[1], reverse=True)
    top_5_id = [word2id_dict[x[0][0]] for x in sorted_centrality[0:5]]
    centrality = np.mean(emb[top_5_id, :], axis=0)

    # Node2Vec
    graph = create_analysis_node(graph)
    node2vec = Node2Vec(graph, workers=4, quiet=True)
    model = node2vec.fit()
    node2vec = model.wv.get_vector('ANALYSIS_NODE')

    return np.concatenate((graph_stats, centrality, node2vec))

def create_analysis_node(G):
    G.add_node("ANALYSIS_NODE")
    for n in G.nodes:
        G.add_edge("ANALYSIS_NODE", n)
    return G

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    graph_generator = GraphGenerator("./data/test/test.txt", emb, word2id_dict, id2word_dict)
    G = graph_generator.generate_graph()
    print(gen_style_vec(G, word2id_dict, emb))
