import pandas as pd
import networkx
import textstat
import textdistance
from itertools import repeat
from statistics import mean
import logging
import math
from nltk.tokenize import word_tokenize
import glove_similarity

if __name__ == '__main__':
    comments = pd.read_csv("data/comments_processed.csv", engine = 'python')
    comments = comments[comments['author'].notna() & comments['author'].notnull()]

    videos = pd.read_csv("data/videos_processed.csv", engine = 'python')
    videos = videos[videos['video_uploader_name'].notna() & videos['video_uploader_name'].notnull()]

    c_v = pd.merge(comments, videos, left_on = ['video_id'], right_on = ['video_id'], how='left')
    c_v = c_v[['cid', 'text', 'votes', 'time', 'author', 'comment_timestamp',
       'video_id', 'search_query', 'date_mined', 'reply', 'text_level',
       'language_x', 'spam', 'video_url', 'video_title', 'video_views', 'video_uploader_id', 'video_uploader_name', 'video_description']]

    #c_v[c_v['video_id'] != c_v['video_id']][['video_id', 'video_id']].__len__()

