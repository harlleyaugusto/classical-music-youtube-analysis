import videos

model = {}

import numpy as np

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


import re
from nltk.corpus import stopwords
import pandas as pd

def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    cleaned_words = list(set([w for w in words if w not in stopword_set]))

    return cleaned_words

def cosine_distance_between_two_words(word1, word2):
    import scipy
    return (1- scipy.spatial.distance.cosine(model[word1], model[word2]))

def calculate_heat_matrix_for_two_sentences(s1,s2):
    s1 = preprocess(s1)
    s2 = preprocess(s2)
    result_list = [[cosine_distance_between_two_words(word1, word2) for word2 in s2] for word1 in s1]
    result_df = pd.DataFrame(result_list)
    result_df.columns = s2
    result_df.index = s1
    return result_df

def cosine_distance_wordembedding_method(s1, s2):
    import scipy
    vector_1 = [model[word] if (word in model) else 0 for word in preprocess(s1)]
    vector_2 = [model[word] if (word in model) else 0 for word in preprocess(s2)]

    vector_1 = np.mean(vector_1, axis = 0) if (vector_1.__len__() > 0) else (0)
    vector_2 = np.mean(vector_2, axis = 0) if (vector_2.__len__() > 0) else (0)


    #vector_1 = np.mean([model[word] if (word in model) else 0 for word in preprocess(s1)],axis=0)
    #vector_2 = np.mean([model[word] if (word in model) else 0  for word in preprocess(s2)],axis=0)


    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    sim = round((1-cosine)*100,2);
    #print(sim)


    #if sim < 0:
    #    print('Cosine: ' + str(sim))
    #    print(str(s1) + '\n')
    #    print(str(s2) + '\n')

    return cosine

def heat_map_matrix_between_two_sentences(s1,s2):
    df = calculate_heat_matrix_for_two_sentences(s1,s2)
    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5,5))
    ax_blue = sns.heatmap(df, cmap="YlGnBu")
    # ax_red = sns.heatmap(df)
    print(cosine_distance_wordembedding_method(s1, s2))
    return ax_blue

def replace(text):
    if text is not None:
        return text.replace('[', '').replace(']', '').replace('\"', '').replace(',', ' ')
    else:
        return ''

if __name__ == '__main__':

    data = pd.read_csv("data/videos.csv")
    data = data[data.relevant]

    # Description cleanning
    data['video_description'] = data['video_description'].apply(videos.remove_ponctuation)

    # description classifier
    data['description_level'] = data['video_description'].apply(videos.length_description).apply(videos.description_classifier)

    # Selecting only description with more than 2 words
    data = data[data.description_level]

    print("Data lenght: " + str(data.__len__()))

    # descriptions = data['video_description'].apply(remove_ponctuation)

    gloveFile = "data/glove.6B.50d.txt"
    model = loadGloveModel(gloveFile)

    list(map(cosine_distance_wordembedding_method, data['video_tags'].apply(replace), data['video_description']))