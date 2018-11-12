#!/usr/bin/env python
from analyze import *
from utils import *
from TextBag import TextBag as GraphGenerator
from multiprocessing import Pool

N_CORES = 4

def vectorize(path):
    bag = GraphGenerator(path, emb, word2id_dict, id2word_dict)
    G = bag.generate_graph()
    G = bag.create_analysis_node(G)
    if nx.number_of_nodes(G) <= 400:
        return gen_style_vec(G)
    else:
        return None

def main():
    global emb, word2id_dict, id2word_dict
    emb, word2id_dict, id2word_dict  = load_embeddings()
    presidents = os.listdir('./data/presidential/')
    p = Pool(N_CORES)
    pres_speeches = []
    for president in presidents:
        text_files = os.listdir('./data/presidential/' + president)
        for speech in text_files:
            path = './data/presidential/' + president + '/' + speech
            pres_speeches += [(president, path)]
    speeches = [x[1] for x in pres_speeches]
    p.map(vectorize, speeches)

    #print([x for x in os.walk('./data/presidential/')])
    #for president in presidents:
    #    vec = 0
    #    for speech in text_files:
    #        path = './data/presidential/' + president + '/' + speech
    #        bag = GraphGenerator(path, emb, word2id_dict, id2word_dict)
    #        G = bag.generate_graph()
    #        vec += gen_style_vec(G)
    #    print(president, vec/len(text_files))

if __name__=="__main__":
    main()
