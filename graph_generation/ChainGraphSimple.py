"""
Graph_Generator.py
Template class specifying generic functions for GraphGenerator
Class
"""
import os, pickle
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import networkx as nx
import nltk

from utils import *
from GraphGenerator import GraphGenerator

class ChainGraphSimple(GraphGenerator):
    def __init__(self, txt_file, emb, word2id, id2word):
        self.emb, self.word2id_dict, self.id2word_dict = emb, word2id, id2word
        self.tokens = self.tokenize(txt_file)
        self.num_meta = 0


    def generate_graph(self):
        tagged = nltk.pos_tag(self.tokens)
        break_inds = [i for i, word in enumerate(tagged) if word[0] in ['.','!','?']]
        G = nx.DiGraph()
        start_ind = 0
        print(tagged)
        for i, ind in enumerate(break_inds):
            self.connect_sentence(tagged[start_ind:ind], G, i)
            start_ind = ind + 1
            if i > 0:
                prev_meta = 'metanode_{}'.format(i-1)
                cur_meta = 'metanode_{}'.format(i)
                G.add_edge(prev_meta, cur_meta)
        self.connect_meta(G)
        return G


    def connect_sentence(self, sentence, G, sent_num):
        # relationship = set(['VB', 'VBD', 'VBN', 'VBP', 'VBZ', 'IN', 'CC']) #ADP is 'adposition'
        determiner = set(['WDT', 'DT', 'PDT'])
        names = set(word[0] + "_{}".format(sent_num) for word in sentence \
                    if word[1] not in determiner)
        for name in names: G.add_node(name)
        src_node = sentence[0][0] + '_{}'.format(sent_num)
        meta_node = "metanode_{}".format(sent_num) # Connects to all other words in sentence
        G.add_node(meta_node)
        self.num_meta += 1
        for word_i in sentence[1:]:
            if word_i[1] in determiner:
                continue
            word = word_i[0] + '_{}'.format(sent_num)
            G.add_edge(src_node, word)
            G.add_edge(meta_node, word)
            src_node = word


    def connect_meta(self, G):
        '''
        Connect the metanodes of sentences that have similarities (measured by dot product)
        75th percentile or greater
        '''
        self.calc_sentence_meanings(G)
        percentile = np.percentile(self.self_sim, 75)
        for i in range(self.num_meta):
            for j, sim in enumerate(self.self_sim[i,:]):
                if i == j: continue
                if sim >= percentile:
                    G.add_edge("metanode_%d" % i, "metanode_%d" % j)


    def calc_sentence_meanings(self, G):
        '''
        Approximate "sentence meaning" by averaging the word vectors of a sentence.
        Reason that the mean normalizes by sentence length, since sentence length
        can be approximated from sentence metanode degree
        '''
        self.meanings = np.zeros((self.num_meta, self.emb.shape[1]))
        for i in range(self.num_meta):
            meaning = np.zeros(self.emb.shape[1])
            cur_sentence = 'metanode_{}'.format(i)
            num_nbr_words = 0
            for nbr in G.neighbors(cur_sentence):
                if 'metanode_' in nbr: continue # skip metanode
                word = nbr[:nbr.find('_')]
                ind = self.word2id(word)
                meaning += self.emb[ind]
                num_nbr_words += 1
            self.meanings[i] = meaning / num_nbr_words
        self.self_sim = np.matmul(self.meanings, self.meanings.T)


if __name__=="__main__":
    emb, word2id_dict, id2word_dict = load_embeddings()
    gen = ChainGraphSimple("test.txt", emb, word2id_dict, id2word_dict)
    G = gen.generate_graph()
    nx.draw_networkx(G)
    plt.show()
