import pandas as pd
import itertools
import networkx as nx
import numpy as np
from scipy import spatial
from networkx import Graph
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib import pylab
from datetime import datetime

import re
import textstat
import textdistance
from itertools import repeat
from statistics import mean
import logging
import math
from nltk.tokenize import word_tokenize
import glove_similarity

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos, node_size=2.6)
    nx.draw_networkx_edges(graph,pos, width = 0.3)
    #nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig



def drawing_network(graph):
    pos = nx.graphviz_layout(graph)

    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    # color by path length from node near center
    p = dict(nx.single_source_shortest_path_length(G, ncenter))

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                           node_size=3,
                           node_color=list(p.values()),
                           cmap=plt.cm.Reds_r)

    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.show()

def network_composer(c_v):
    G = []
    edges = []
    past_composer = ""
    composer_group = c_v.groupby(['composer_name','video_id'])
    for name, grp in composer_group:
        print("Composer: " + str(name[0]) + " Video: " + name[1])
        author = grp['author'].apply(str).unique()
        tuples = list(itertools.combinations(author, 2))
        edges.append(tuples)
        edges = list(itertools.chain.from_iterable(edges))
        edges = list(set(edges))

        if(past_composer != name[0] and past_composer != ""):
            g = nx.Graph()
            edges = list(filter(lambda x: isinstance(x, tuple), edges))
            g.add_edges_from(edges)
            G.append((name[0],g))
            edges = []
            past_composer = name[0]
        else:
            past_composer = name[0]
    return G

def to_float(f):
    try:
        if(f is not None or f):
            return float(f)
        else:
            return None
    except Exception:
        return None

def to_int(i):
    try:
        if (i is not None):
            return int(i)
        else:
            return None
    except Exception:
        return None


def to_date(d):
    if (d is not None) and (not math.isnan(d)):
        return  datetime.fromtimestamp(d)
    else:
        return None

if __name__ == '__main__':
    comments = pd.read_csv("data/comments_processed.csv", engine = 'python', encoding = "utf-8")
    comments = comments[comments['author'].notna() & comments['author'].notnull()]

    videos = pd.read_csv("data/videos_processed.csv", engine = 'python')
    videos = videos[videos['video_uploader_name'].notna() & videos['video_uploader_name'].notnull()]

    c_v = pd.merge(comments, videos, left_on = ['video_id'], right_on = ['video_id'], how='inner')

    c_v = c_v[['cid', 'text', 'votes', 'time', 'author',  'video_uploader_id', 'video_uploader_name', 'comment_timestamp',
       'video_id', 'search_query', 'date_mined', 'reply', 'text_level',
       'language_x', 'spam', 'video_url', 'video_title', 'video_views', 'video_description', 'composer_name']]
    c_v['date'] = c_v.comment_timestamp.apply(to_float).apply(to_int).apply(to_date)
    c_v['date_index'] = pd.to_datetime(c_v['date'])

    video_group = c_v.groupby('video_id')
    c_v = c_v.set_index('date_index')

    count = 1
    total = 0
    edges = []

    a = c_v.groupby(['composer_name', 'video_id', pd.Grouper(freq='M')])

    for name, group in a:
        print(str(name[0]) + " " + str(name[1]) + " " + (str(name[2])))

    '''
    for name, grp in video_group:
        author = grp['author'].apply(str).unique()
        tuples = list(itertools.combinations(author, 2))
        print('Name: ' + name + ' Count: ' + str(count) + ' tuples.len: ' + str(tuples.__len__()))
        edges.append(tuples)
        edges = list(itertools.chain.from_iterable(edges))
        edges = list(set(edges))
        total = total + tuples.__len__()
        #G.add_edges_from(tuples)

        count = count +1

    edges = list(filter(lambda x: isinstance(x, tuple), edges))
    G = nx.Graph()
    G.add_edges_from(edges)
    drawing_network(G)

    '''

    Gs = network_composer(c_v)

    #fOk8Tm815lE

    #timeserie = c_v.groupby(['composer', 'id_video', ''])