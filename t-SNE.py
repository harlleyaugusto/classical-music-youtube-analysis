import logging
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    data = pd.read_csv("data/user_profile.csv")

    logging.info('Data loaded!')

    np.random.seed(42)
    rndperm = np.random.permutation(data.shape[0])

    #set a random of users. If n == data.__len__(), then using all users.
    N = 10000#data.__len__()
    data_subset = data.loc[rndperm[:N], :].copy()

    data_values = data_subset.drop(['video_uploader_id','composer_name'], axis=1).values

    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)

    tsne_results = tsne.fit_transform(data_values)

    data_subset['tsne-2d-one'] = tsne_results[:, 0]
    data_subset['tsne-2d-two'] = tsne_results[:, 1]

    plt.figure(figsize=(16, 16))
    sns_plot = sns.scatterplot(
        x="tsne-2d-one", y="tsne-2d-two",
        #hue="composer_name",
        #palette=sns.color_palette("hls", 10),
        data=data_subset,
        legend="full",
        alpha=0.9
    )
    plt.savefig('random_users_'+str(N)+'_t-sne.png')
