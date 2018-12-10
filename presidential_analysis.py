
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
        print(path)
        if generator == 'bag':
            graph_generator = TextBag(path, emb, word2id_dict, id2word_dict)
        elif generator == 'window':
            graph_generator = TextWindow(path, emb, word2id_dict, id2word_dict)
        elif generator == 'pos':
            graph_generator = TextPOS(path, emb, word2id_dict, id2word_dict)
        elif generator == 'chain':
            graph_generator = ChainGraphSimple(path, emb, word2id_dict, id2word_dict)
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

    presidents = os.listdir('./data/presidential/')
    p = Pool(N_CORES)
    pres_speeches = []
    with open('paths.txt', 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            pres_speeches.append(line)

    #for president in presidents:
    #    text_files = os.listdir('./data/presidential/' + president)
    #    for speech in text_files:
    #        path = './data/presidential/' + president + '/' + speech
    #        pres_speeches += [(president, path)]
    speeches = [x[1] for x in pres_speeches]
    finished = list(map(vectorize, speeches))
    vectors = [(pres, file, finished[i]) for i, (pres, file) in enumerate(pres_speeches) if finished[i] is not None]
    pres = [x[0] for x in vectors]
    X = np.concatenate([x[2][:,np.newaxis] for x in vectors], axis=1)
    times = [president_metadata.president2date[x] for x in pres]
    bool_vec = [float(x > 1900) for x in times]
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
            df.to_csv("results_betweeness.csv")
if __name__=="__main__":
    main()
