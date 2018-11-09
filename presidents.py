#!/usr/bin/env python
from analyze import *
from utils import *
from TextBag import TextBag as GraphGenerator


def main():
    emb, word2id_dict, id2word_dict  = load_embeddings()
    presidents = os.listdir('./data/presidential/')
    #print([x for x in os.walk('./data/presidential/')])
    for president in presidents:
        text_files = os.listdir('./data/presidential/' + president)
        vec = 0
        for speech in text_files:
            path = './data/presidential/' + president + '/' + speech
            bag = GraphGenerator(path, emb, word2id_dict, id2word_dict)
            G = bag.generate_graph()
            vec += gen_style_vec(G)
        print(president, vec/len(text_files))

if __name__=="__main__":
    main()
