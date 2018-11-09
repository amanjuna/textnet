'''
StyleGraph.py

Defines the StyleGraph class - a SNAP graph constructed by a GraphGenerator
that contains associated metadata
'''

import os

import snap

class StyleGraph():

    def __init__(self, name, directed=False):
        self.name = name
        if directed:
            self.graph = snap.TNGraph.New()
        else:
            self.graph = snap.TUNGraph().New()
        self.int_to_str = {}
        self.str_to_int = {}

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
        #with open()


    def load(self, graph_folder):
        graph_path = os.path.join(graph_folder, 'graph.txt')
        meta_path = os.path.join(graph_foler, 'meta.json')
        self.graph = snap.LoadEdgeList(snap.PUNGraph, graph_path, 0, 1)
        self.meta_from_dict(meta_path)

    def add_node(self, int_id, str_id):
        self.graph.AddNode(int_id)
        self.int_to_str[int_id] = str_id
        self.str_to_int[str_id] = int_id



    def meta_from_dict(self, path):
        pass
