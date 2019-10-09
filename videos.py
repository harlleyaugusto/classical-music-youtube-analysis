import pandas as pd
import textstat
import string

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

    descriptions = data['video_description'].apply(remove_ponctuation)
    readability_fre = descriptions.apply(lambda text: textstat.flesch_reading_ease(text) if (text is not None) else text)

    l_d = descriptions.apply(length_description)



    data['flesch_reading_ease'] = list(readability_fre)
    data['description_length'] = list(l_d)
    data['description_level'] = l_d.apply(description_classifier)

    #composer_uploaders = data.groupby(['video_uploader_id', 'composer_name']).count()
    #s_sum =  data.groupby('video_uploader_id').sum()

    # Completeness calculation
    # comp = []
    # for index, row in data.iterrows():
    #     print(str(index) + "/" + str (data.__len__()))
    #     comp.append(completeness(row))

    # u = list(uploaders.index)
    # up = list(uploaders.iloc[:,0])
    # l = list(s_sum.iloc[:,1])
    # d = list(s_sum.iloc[:,2])
    # c = list(s_sum.iloc[:,6])
    #
    # df = {'user_id': u, 'user_count': up, 'user_likes': l, 'user_dislike': d, 'user_comments': c}
    #
    # df = pd.DataFrame(df)
    # df.to_csv("data/s_videos.csv", index = False)
