import pandas as pd
import textstat
import textdistance
from itertools import repeat
from statistics import mean
import logging
import math
from nltk.tokenize import word_tokenize
from src.models import glove_similarity
import src.util.config as config

def completeness(video):
    if video is not None:
        total = video[video.notnull()].__len__()
        if video['video_tags'] is not None or video['video_tags'].__len__() == 0:
            total = total - 1
        if video['video_categories'] is not None or video['video_categories'].__len__() == 0:
            total = total - 1
        return total / video.keys().__len__()
    else:
         return 0


def length_description(text):
    if text is not None and isinstance(text, str):
        return word_tokenize(text).__len__()
    else:
        return 0

def description_classifier(len):
    if(len == 0 or len == 1):
        return False
    else:
        return True


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    c = config.Config()

    data = pd.read_csv(c.data_dir + c.processed_data + "videos_processed.csv")

    logging.info('Data loaded!')

    gloveFile = c.data_dir + c.external_data + c.glove
    model = glove_similarity.loadGloveModel(gloveFile)

    logging.info('glove model built!')

    logging.info('Calculating similarity between...')

    #sim = []
    #for index, row in data.iterrows():
    #    sim.append(glove_similarity.cosine_distance_wordembedding_method(model, glove_similarity.replace(row.video_tags), row.video_description))
    sim = list(map(glove_similarity.cosine_distance_wordembedding_method, repeat(model), data.video_tags.apply(
        glove_similarity.replace), data.video_description))

    logging.info('Done!')

    data['sim_tag_description'] = [0 if math.isnan(x) or x < 0 else x for x in sim]

    #Completeness calculation
    comp = [completeness(row) for index, row in data.iterrows()]

    #Readability
    readability_fre = data['video_description'].apply(lambda text: textstat.flesch_reading_ease(text) if (text is not None) else text)
    #
    #Description length
    l_d = data['video_description'].apply(length_description)

    data['completeness'] = list(comp)
    data['flesch_reading_ease'] = list(readability_fre)
    data['description_length'] = list(l_d)


    #Consine beteween each video's tags and video's composer
    consine_lst = []
    for index, row in data.iterrows():
        l = eval(row.video_tags)
        consine_lst.append(list(map(textdistance.cosine, l, list(repeat(row.composer_name, l.__len__())))))

    #Mean of the three greater similarities beteween composer and all tags
    mean_cosine = [mean(sorted(i, reverse=True)[0:3]) if (i.__len__() > 0) else 0 for i in consine_lst]

    data['sim_tag_composer'] = mean_cosine

    uploaders_group = data[data.description_level].groupby(['video_uploader_id', 'composer_name'])

    uploaders_count = uploaders_group[['video_url', 'video_likes', 'video_dislikes', 'video_comments', 'video_views']].count()

    uploaders_count = uploaders_count.rename(columns={"video_url": "video_count"})

    uploaders_avg = uploaders_group[['completeness','flesch_reading_ease', 'description_length', 'sim_tag_composer', 'sim_tag_description']].mean()

    user_profile = pd.merge(uploaders_count, uploaders_avg, left_index=True, right_index=True)

    user_profile.to_csv(c.data_dir + c.processed_data + "user_profile.csv")

