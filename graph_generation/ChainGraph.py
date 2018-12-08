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

class ChainGraph(GraphGenerator):
    def __init__(self, txt_file, emb, word2id, id2word, is_file=True):
        self.emb, self.word2id_dict, self.id2word_dict = emb, word2id, id2word
        self.tokens = self.tokenize(txt_file, is_file)


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
        for word_i in sentence[1:]:
            if word_i[1] in determiner:
                continue
            word = word_i[0] + '_{}'.format(sent_num)
            G.add_edge(src_node, word)
            G.add_edge(meta_node, word)
            src_node = word


    def tokenize(self, txt_file, is_file=True):
        tokens = []
        n_unk, n_word = 0, 0
        if is_file:
            with open(txt_file, 'r') as open_doc:
                for line in open_doc:
                    for token in nltk.word_tokenize(line):
                        lower = token.lower()
                        n_word += 1
                        if lower in self.word2id_dict:
                            tokens += [lower]
                        else:
                            tokens += ["UNK"]
                            n_unk += 1
        else:
            for token in nltk.word_tokenize(txt_file):
                lower = token.lower()
                n_word += 1
                if lower in self.word2id_dict:
                    tokens += [lower]
                else:
                    tokens += ["UNK"]
                    n_unk += 1
        print("Unk percentage:", n_unk/n_word)
        return tokens


    def word2id(self, word):
        return self.word2id_dict[word]

    def id2word(self, id):
        return self.id2word_dict[id]

if __name__=="__main__":
    emb, word2id_dict, id2word_dict = load_embeddings()
    gen = ChainGraph("test.txt", emb, word2id_dict, id2word_dict)
    G = gen.generate_graph()
    nx.draw_networkx(G)
    plt.show()
