import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv("data/videos.csv")
    uploaders = data.groupby('video_uploader_id').count()
    s_sum =  data.groupby('video_uploader_id').sum()
    #
    u = list(uploaders.index)
    up = list(uploaders.iloc[:,0])
    l = list(s_sum.iloc[:,1])
    d = list(s_sum.iloc[:,2])
    c = list(s_sum.iloc[:,6])

    df = {'user_id': u, 'user_count': up, 'user_likes': l, 'user_dislike': d, 'user_comments': c}

    df = pd.DataFrame(df)
    df.to_csv("data/s_videos.csv", index = False)
