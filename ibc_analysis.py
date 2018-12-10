
import csv
import pandas as pd
from analyze import *
from utils import *
import data.president_metadata as president_metadata
from graph_generation.TextPOS import TextPOS as TextPOS
from graph_generation.TextBag import TextBag as TextBag
from graph_generation.TextWindow import TextWindow as TextWindow
from graph_generation.ChainGraphSimple import ChainGraphSimple as ChainGraphSimple
from multiprocessing import Pool
import json, pickle, treeUtil
N_CORES = 8

generator_g, analysis_g, emb_g, word2id_dict_g, id2word_dict_g = None, None, None, None, None

def vectorize(path):
    print(generator_g)
    if generator_g == 'bag':
        graph_generator = TextBag(path, emb_g, word2id_dict_g, id2word_dict_g)
    elif generator_g == 'window':
        graph_generator = TextWindow(path, emb_g, word2id_dict_g, id2word_dict_g)
    elif generator_g == 'pos':
        graph_generator = TextPOS(path, emb_g, word2id_dict_g, id2word_dict_g)
    elif generator_g == 'chain':
        graph_generator = ChainGraphSimple(path, emb_g, word2id_dict_g, id2word_dict_g)
    else:
        crash()
    G = graph_generator.generate_graph()
    return gen_style_vec(G, word2id_dict_g, emb_g, analysis_g, generator_g)

def run_analyses(generator, analysis, emb, word2id_dict, id2word_dict):

    def vectorize(path):
        if generator == 'bag':
            graph_generator = TextBag(path, emb, word2id_dict, id2word_dict, is_file=False)
        elif generator == 'window':
            graph_generator = TextWindow(path, emb, word2id_dict, id2word_dict, is_file=False)
        elif generator == 'pos':
            graph_generator = TextPOS(path, emb, word2id_dict, id2word_dict, is_file=False)
        elif generator == 'chain':
            graph_generator = ChainGraphSimple(path, emb, word2id_dict, id2word_dict, is_file=False)
        else:
            crash()
        G = graph_generator.generate_graph()
        #if nx.number_of_nodes(G) <= 400:
        #    with open("paths.txt", 'a+') as file:
        #        csv_writer = csv.writer(file)
        #        csv_writer.writerow([path])
        return gen_style_vec(G, word2id_dict, emb, analysis, generator)
        #else:
        #    return None


    [lib, con, neutral] = pickle.load(open('./data/ibc/sampleData.pkl', 'rb'))
    sentences = [('lib', tree.get_words()) for tree in lib] + [('neutral', tree.get_words()) for tree in neutral] + [('con', tree.get_words()) for tree in con]
    text_entries = [x[1] for x in sentences if x[0] != 'neutral']
    finished = list(map(vectorize, text_entries))
    sentences = [x for x in sentences if x[0] != "neutral"]

    vectors = [(bias, finished[i]) for i, (bias, _) in enumerate(sentences) if finished[i] is not None
           and np.sum(finished[i]) < float('inf')]
    bias = [x[0] for x in vectors]
    X = np.concatenate([x[1][:,np.newaxis] for x in vectors], axis=1)
    bool_vec = [x == 'con' for x in bias]
    return get_score(bool_vec, X.T, 2)

def main():
    emb, word2id_dict, id2word_dict  = load_embeddings()
    generators = ['pos', 'bag', 'window', 'chain']
    analyses = ['c', 'n', 'r', 'cr']

    df = pd.DataFrame(index=analyses, columns=generators)
    for graph_generator in generators:
        for analysis in analyses:
            #if graph_generator == 'pos': continue
            print(graph_generator, analysis)
            result = run_analyses(graph_generator, analysis, emb, word2id_dict, id2word_dict)
            df[graph_generator][analysis] = result
            print(result)
            #df.to_csv("results.csv")
            df.to_csv("results_ibc.csv")
if __name__=="__main__":
    main()
