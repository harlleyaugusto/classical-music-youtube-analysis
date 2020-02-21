import numpy as np
import scipy

import re
from nltk.corpus import stopwords
import pandas as pd
from itertools import repeat
import nltk

from src.util import config


def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model


def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    cleaned_words = list(set([w for w in words if w not in stopword_set]))

    return cleaned_words


def cosine_distance_wordembedding_method(model, s1, s2):

    vector_1 = [model[word] if (word in model) else 0 for word in preprocess(s1)]
    vector_2 = [model[word] if (word in model) else 0 for word in preprocess(s2)]

    #print("1: ", vector_1, "\n 2: ", vector_2)

    vector_1 = np.mean(vector_1, axis = 0) if (vector_1.__len__() > 0) else (0)
    vector_2 = np.mean(vector_2, axis = 0) if (vector_2.__len__() > 0) else (0)

    #print("1: ", vector_1, "\n 2: ", vector_2)

    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    sim = round((1-cosine)*100,2);


    return sim

def replace(text):
    if text is not None:
        return text.replace('[', '').replace(']', '').replace('\"', '').replace(',', ' ')
    else:
        return ''

if __name__ == '__main__':
    c = config.Config()

    data = pd.read_csv(c.data_dir + c.processed_data + "videos_processed.csv")
    gloveFile = c.data_dir + c.external_data + c.glove
    model = loadGloveModel(gloveFile)

    #a = list(map(teste, cycle('teste'), data['video_tags'].apply(replace), data['video_description']))
    #print('Model len:' + str(len(model)))
    #sim =[]
    #for index, row in data.iterrows():
    #    sim.append(cosine_distance_wordembedding_method(model, replace(row.video_tags),row.video_description))

    sim = list(map(cosine_distance_wordembedding_method, repeat(model), data.video_tags.apply(replace), data.video_description))

   # sim = list(map(cosine_distance_wordembedding_method, cycle(model), data['video_tags'].apply(replace), data['video_description']))

   #nan_values[nan_values != '[]'] nan values for similarity
   #video_tags_nan_values = nan_values[nan_values['video_tags'] != '[]']['video_tags']
   # video_description_nan_values = nan_values[nan_values['video_description'] != '[]'][['video_description', 'video_id']]
   #video descripiton for [] tags
    #videos_mais_que_uma_tag = nan_values[nan_values['list_tags'].apply(lambda l: True if (l.__len__() > 1) else False)][['video_tags', 'video_description']]
    #video description and video tags for videos with more than 1 tag

