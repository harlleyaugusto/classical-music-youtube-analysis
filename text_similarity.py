from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess
import numpy as np


desc = ['Japan Japan has some great novelists. Who is your favorite Japanese writer?']
title = 'Japan has some great novelists. Who is your favorite Japanese writer?'

desc_split = [word_tokenize(text) for text in desc]

dictionary = corpora.Dictionary(desc_split)
#dictionary = corpora.Dictionary(simple_preprocess(desc, deacc = True))

feature_cnt = len(dictionary)

corpus = [dictionary.doc2bow(text) for text in desc_split]

tfidf = models.TfidfModel(corpus)

kw_vector = dictionary.doc2bow(word_tokenize(title))

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)

sim = index[tfidf[kw_vector]]

for i in range(len(sim)):
    print('keyword is similar to text%d: %.2f' % (i + 1, sim[i]))

#if __name__ == '__main__':


#    text_similarity(desc, title)