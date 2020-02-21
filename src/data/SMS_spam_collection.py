import string

import pandas as pd
import csv
import logging

from langdetect import detect

from src.util import config

if __name__ == '__main__':

    c = config.Config()

    data = pd.read_csv(c.data_dir + c.external_data + "spam_detection/SMSSpamCollection", engine='python', sep='\t', quoting=3)
    data.columns = ['CLASS', 'CONTENT']
    data['CLASS'] = data['CLASS'].apply(lambda c: 1 if (c == 'spam') else 0)

    a =  pd.DataFrame()
    a['COMMENT_ID'] = None
    a['AUTHOR'] = None
    a['DATE'] = None
    a['CONTENT'] = data['CONTENT']
    a['CLASS'] = data['CLASS']


    a.to_csv(c.data_dir + c.external_data + "spam_detection/SMSSpamCollection.csv", index=False)

    #COMMENT_ID, AUTHOR, DATE, CONTENT, CLASS