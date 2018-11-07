'''
StyleGraph.py

Defines the StyleGraph class - a SNAP graph constructed by a GraphGenerator
that contains associated metadata
'''

import os

import snap

class StyleGraph():

    def __init__(self, name):
        self.name = name
        self.graph = snap.PUNGraph().New()


    def save(self):
        '''
        Writes graph data to file

        Creates a folder named self.name, and creates 2 files:
        - graph.txt, which contains the edge list for the SNAP graph
        - meta.json, which contains all other data
        '''
        folder = self.name
        os.mkdir(os.path.join('graphs', folder))
        meta = {}
        for key in self.__dict__.keys():
            to_write[key] = self.__dict__[key]
        to_write.remove('graph')
        with open()


    def load(self, graph_folder):
        graph_path = os.path.join(graph_folder, 'graph.txt')
        meta_path = os.path.join(graph_foler, 'meta.json')
        self.graph = snap.LoadEdgeList(snap.PUNGraph, graph_path, 0, 1)
        self.meta_from_dict(meta_path)


    def meta_from_dict(self, path):
        pass
