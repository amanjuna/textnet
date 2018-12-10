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
import sklearn.cluster

def gen_style_vec(graph, word2id_dict, emb, analysis, generator, n_samples=100):
    '''
    Given StyleGraph, return a style vector
    '''
    # Graph stats
    def get_graph_stats():
        n_nodes = nx.number_of_nodes(graph)
        if n_nodes < n_samples:
            n_samples = n_nodes
        random_sample = random.sample(graph.nodes(), n_samples)
        avg_degree = np.mean([x[1] for x in graph.degree(random_sample)])
        avg_cluster = nx.average_clustering(graph, random_sample)
        graph_stats = np.array([avg_degree, avg_cluster])

    # Centrality
    def get_centrality(graph):
        #centrality = nx.betweenness_centrality(graph)
        centrality = nx.eigenvector_centrality_numpy(graph)
        #centrality = nx.harmonic_centrality(graph)
        sorted_centrality = sorted(centrality.items(), key=lambda x:x[1], reverse=True)
        if generator == 'pos' or generator == 'chain':
            sorted_centrality = [x for x in sorted_centrality if "metanode_" not in x[0][0]]
            top_5_id = [word2id_dict[x[0][0]] for x in sorted_centrality[0:5]]
        else:
            top_5_id = [word2id_dict[x[0]] for x in sorted_centrality[0:5]]
        centrality = np.mean(emb[top_5_id, :], axis=0)
        return centrality

    def get_random(graph):
        #centrality = nx.betweenness_centrality(graph)
        centrality = nx.eigenvector_centrality_numpy(graph)
        #centrality = nx.harmonic_centrality(graph)
        sorted_centrality = sorted(centrality.items(), key=lambda x:x[1], reverse=True)
        if generator == "pos" or generator == 'chain':
            sorted_centrality = [x for x in sorted_centrality if "metanode_" not in x[0]]
            top_5_id = [word2id_dict[x[0][0]] for x in random.sample(sorted_centrality, 5)]
        else:
            top_5_id = [word2id_dict[x[0]] for x in random.sample(sorted_centrality, 5)]
        centrality = np.mean(emb[top_5_id, :], axis=0)
        return centrality

    # Node2Vec
    def get_node2vec(graph):
        graph = create_analysis_node(graph)
        node2vec = Node2Vec(graph, p=1, q=3, workers=8, quiet=True)
        model = node2vec.fit()
        node2vec = model.wv.get_vector('ANALYSIS_NODE')
        return node2vec

    #graph_stats = get_graph_stats()
    if analysis == "c":
        return get_centrality(graph)
    if analysis == "n":
        return get_node2vec(graph)
    if analysis == 'r':
        return get_random(graph)
    if analysis == 'cr':
        centrality = get_centrality(graph)
        node2vec = get_node2vec(graph)
        return np.concatenate((centrality, node2vec))

def create_analysis_node(G):
    G.add_node("ANALYSIS_NODE")
    for n in G.nodes:
        G.add_edge("ANALYSIS_NODE", n)
    return G

def get_score(ground_truth_labels, node_vecs, n_classes):
    res = sklearn.cluster.KMeans(n_clusters = n_classes, n_init=100).fit(node_vecs)

    precision = max(sklearn.metrics.precision_score(ground_truth_labels, res.labels_), sklearn.metrics.precision_score([x == 0 for x in ground_truth_labels], res.labels_))
    recall = max(sklearn.metrics.recall_score(ground_truth_labels, res.labels_), sklearn.metrics.recall_score([x == 0 for x in ground_truth_labels], res.labels_))

    #print(sklearn.metrics.precision_score(ground_truth_labels, res.labels_), sklearn.metrics.recall_score(ground_truth_labels, res.labels_))
    metric1 = sum([x == ground_truth_labels[i] for i, x in enumerate(res.labels_)])/len(ground_truth_labels)
    metric2 = sum([x != ground_truth_labels[i] for i, x in enumerate(res.labels_)])/len(ground_truth_labels)
    return max(metric1, metric2), precision, recall#sklearn.metrics.adjusted_mutual_info_score(res.labels_, ground_truth_labels)

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    graph_generator = GraphGenerator("./data/test/test.txt", emb, word2id_dict, id2word_dict)
    G = graph_generator.generate_graph()
    print(gen_style_vec(G, word2id_dict, emb))
