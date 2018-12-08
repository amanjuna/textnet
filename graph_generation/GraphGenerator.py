"""
Graph_Generator.py

Template class specifying generic functions for GraphGenerator
Class

"""

from utils import *
import numpy as np
import os, pickle, nltk
import networkx as nx

class GraphGenerator:
    def __init__(self, txt_file, emb, word2id, id2word, is_file=True):
        self.emb, self.word2id_dict, self.id2word_dict = emb, word2id, id2word
        self.tokens = self.tokenize(txt_file, is_file)

    def generate_graph(self):
        print("Needs to be called on a child of the GraphGenerator Class")
        pass

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

    def create_analysis_node(self, G):
        G.add_node("ANALYSIS_NODE")
        for n in G.nodes:
            G.add_edge("ANALYSIS_NODE", n)
        return G


    def word2id(self, word):
        return self.word2id_dict[word]

    def id2word(self, id):
        return self.id2word_dict[id]

if __name__=="__main__":
    emb, word2id_dict, id2word_dict  = load_embeddings()
    gg = GraphGenerator("gita.txt", emb, word2id_dict, id2word_dict)
    #gg.load_embeddings()
