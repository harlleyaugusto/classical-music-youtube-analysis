import pandas as pd
import itertools
import networkx as nx
from networkx import Graph
from copy import deepcopy

import matplotlib.pyplot as plt
import re
import textstat
import textdistance
from itertools import repeat
from statistics import mean
import logging
import math
from nltk.tokenize import word_tokenize
import glove_similarity


if __name__ == '__main__':
    comments = pd.read_csv("data/comments_processed.csv", engine = 'python', encoding = "utf-8")
    comments = comments[comments['author'].notna() & comments['author'].notnull()]

    videos = pd.read_csv("data/videos_processed.csv", engine = 'python')
    videos = videos[videos['video_uploader_name'].notna() & videos['video_uploader_name'].notnull()]

    c_v = pd.merge(comments, videos, left_on = ['video_id'], right_on = ['video_id'], how='left')
    c_v = c_v[['cid', 'text', 'votes', 'time', 'author',  'video_uploader_id', 'video_uploader_name', 'comment_timestamp',
       'video_id', 'search_query', 'date_mined', 'reply', 'text_level',
       'language_x', 'spam', 'video_url', 'video_title', 'video_views', 'video_description']]

    video_group = c_v.groupby('video_id')

    count = 1
    total = 0
    edges = []

    for name, grp in video_group:
        tuples = list(itertools.combinations(grp['author'].unique(), 2))
        print('Name: ' + name + ' Count: ' + str(count) + ' tuples.len: ' + str(tuples.__len__()))
        edges.append(tuples)
        edges = list(itertools.chain.from_iterable(edges))
        edges = list(set(edges))
        total = total + tuples.__len__()
        #G.add_edges_from(tuples)

        count = count +1
    print(total)
    G = nx.Graph()
    G.add_edges_from(tuples)

    edges = list(filter(lambda x: isinstance(x, tuple), edges))

    #fOk8Tm815lE