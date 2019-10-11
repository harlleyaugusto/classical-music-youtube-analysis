import pandas as pd
import textstat
import string
import textdistance
import itertools
from itertools import cycle
from itertools import repeat
from statistics import mean


def completeness(video):
    if video is not None:
         return video[video.notnull()].__len__() / video.keys().__len__()
    else:
         return 0

def remove_ponctuation(text):
    if text is not None and isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    else:
        None

def length_description(text):
    if text is not None and isinstance(text, str):
        return text.__len__()
    else:
        return 0

def description_classifier(len):
    if(len == 0 or len == 1):
        return False
    else:
        return True


if __name__ == '__main__':
    data = pd.read_csv("data/videos.csv")
    data = data[data.relevant]

    #Completeness calculation
    comp = []
    for index, row in data.iterrows():
        print(str(index) + "/" + str (data.__len__()))
        comp.append(completeness(row))

    descriptions = data['video_description'].apply(remove_ponctuation)
    readability_fre = descriptions.apply(lambda text: textstat.flesch_reading_ease(text) if (text is not None) else text)

    l_d = descriptions.apply(length_description)

    data['completeness'] = list(comp)
    data['flesch_reading_ease'] = list(readability_fre)
    data['description_length'] = list(l_d)
    data['description_level'] = l_d.apply(description_classifier)

    #Mean consine
    t = []
    for index, row in data.iterrows():
        l = eval(row.video_tags)
        t.append(list(map(textdistance.cosine, l, list(repeat(row.composer_name, l.__len__())))))

    mean_cosine = [mean(sorted(i, reverse=True)[0:3]) if (i.__len__() > 0) else 0 for i in t]

    data['mean_consine'] = mean_cosine

    uploaders_group = data[data.description_level].groupby(['video_uploader_id', 'composer_name'])

    uploaders_count = uploaders_group[['video_url', 'video_likes', 'video_dislikes', 'video_comments', 'video_views']].count()

    uploaders_count = uploaders_count.rename(columns={"video_url": "video_count"})

    uploaders_avg = uploaders_group[['completeness','flesch_reading_ease', 'description_length']].mean()

    user_profile = pd.merge(uploaders_count, uploaders_avg, left_index=True, right_index=True)



    user_profile.to_csv("data/user_profile.csv")

    #data[a.apply(lambda text: 'Music' not in text if (text is not None and isinstance(text, str)) else False)]
    #max(list(map(textdistance.cosine, data.video_tags.apply(eval), cycle(data.composer_name))))
    #data.video_tags.apply(eval).apply(lambda list_tags: list(map(textdistance.cosine, cycle(data.composer_name))))
    #data.loc[0:2, 'video_tags'].apply(eval).apply(lambda list_tag: list(map(textdistance.cosine, list_tag, data.loc[0:2, 'composer_name'].apply(cycle))))

    #step1.apply(lambda list_tag: list(map(textdistance.cosine, list_tag, data.loc[0:2, 'composer_name'].apply(lambda name: repeat(name, list_tag.__len__())))))

    #step1 = data.loc[0:2, 'video_tags'].apply(eval)
    #step1.apply(lambda lt: list(map(textdistance.cosine, lt, cycle(['blah']))))

