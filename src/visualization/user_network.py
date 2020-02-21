import pandas as pd
import itertools
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib import pylab
from datetime import datetime
import logging

import math
import time

from src.util import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def network_videos(c_v):
    '''
    edges = []
    video_group = c_v.groupby('video_id')
    for name, grp in video_group:
        author = grp['author'].unique()
        tuples = list(itertools.combinations(author, 2))
        tuples = list(filter(lambda x: isinstance(x, tuple), tuples))
        #edges.append(tuples)
        edges = edges + tuples
        size_edges = edges.__len__()
        #edges = list(itertools.chain.from_iterable(edges))
        edges = list(set(edges))
        size_edges = edges.__len__()
        logger.info('video_id: ' + name + ' edges: ' + str(edges.__len__()))

    #edges = list(filter(lambda x: isinstance(x, tuple), edges))
    logger.info(' edges: ' + str(edges.__len__()))
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

    '''
    video_group = c_v.groupby('video_id')
    t_agg = video_group.aggregate(
        {
            'author': lambda authors: list(itertools.combinations(authors.unique(), 2))
        }
    )[['author']]

    t_agg = t_agg.author.apply(lambda l: list(set(l)))
    lst_a = list(itertools.chain.from_iterable(t_agg))
    lst_a = list(set(lst_a))

    lst_a = list(filter(lambda x: isinstance(x, tuple), lst_a))

    print(lst_a.__len__())

    G = nx.Graph()
    G.add_edges_from(lst_a)

    return G
def network_composer_v2(c_v):
   G = []
   edges = []
   past_composer = ""
   composer_group = c_v.groupby(['composer_name','video_id'])
   for name, grp in composer_group:
       #logger.info("Composer: " + str(name[0]) + " Video: " + name[1])
       if (past_composer != name[0] and past_composer != ""):
           g = nx.Graph()
           edges = list(filter(lambda x: isinstance(x, tuple), edges))
           g.add_edges_from(edges)
           logger.info('Composer: ' + str(past_composer) + ' edges: ' + str(g.number_of_edges()))
           G.append((past_composer, g))
           edges = []
           past_composer = name[0]
       else:
           past_composer = name[0]

       author = grp['author'].apply(str).unique()
       tuples = list(itertools.combinations(author, 2))
       edges = edges + tuples
       #edges = list(itertools.chain.from_iterable(edges))
       edges = list(set(edges))

   g = nx.Graph()
   edges = list(filter(lambda x: isinstance(x, tuple), edges))
   g.add_edges_from(edges)
   logger.info('Composer: ' + str(past_composer) + ' edges: ' + str(g.number_of_edges()))
   G.append((past_composer, g))

   return G


def network_composer(c_v):
    composer_group = c_v.groupby(['composer_name', 'video_id'])

    composer_agg = composer_group.aggregate(
        {
            'author': lambda authors: list(itertools.combinations(authors.unique(), 2))
        }
    )[['author']]

    composer_agg = composer_agg.reset_index().groupby('composer_name').sum()[['author']]
    composer_agg = composer_agg.author.apply(lambda g: nx.Graph(g))

    return list(composer_agg)

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


def network_time_serie(c_v):
    # Timestamp into datetime
    c_v['date'] = c_v.comment_timestamp.apply(to_float).apply(to_int).apply(to_date)
    c_v['date_index'] = pd.to_datetime(c_v['date'])
    c_v = c_v.set_index('date_index')

    a = c_v.groupby(['composer_name', 'video_id', pd.Grouper(freq='M')])

    for name, group in a:
        print(str(name[0]) + " " + str(name[1]) + " " + (str(name[2])))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    c = config.Config()

    comments = pd.read_csv(c.data_dir + c.processed_data + "comments_processed.csv", engine = 'python', encoding = "utf-8")
    comments = comments[comments['author'].notna() & comments['author'].notnull()]

    videos = pd.read_csv(c.data_dir + c.processed_data + "videos_processed.csv", engine = 'python')
    videos = videos[videos['video_uploader_name'].notna() & videos['video_uploader_name'].notnull()]

    c_v = pd.merge(comments, videos, left_on = ['video_id'], right_on = ['video_id'], how='inner')

    c_v = c_v[['cid', 'text', 'votes', 'time', 'author',  'video_uploader_id', 'video_uploader_name', 'comment_timestamp',
       'video_id', 'search_query', 'date_mined', 'reply', 'text_level',
       'language_x', 'spam', 'video_url', 'video_title', 'video_views', 'video_description', 'composer_name']]


    #gv = network_videos(c_v)

    start_time = time.time()
    gc = network_composer(c_v)
    print("--- %s seconds ---" % (time.time() - start_time))

    #start_time = time.time()
    #gc = network_composer_v2(c_v)
    #print("--- %s seconds ---" % (time.time() - start_time))

    #gts = network_time_serie(c_v)



    
