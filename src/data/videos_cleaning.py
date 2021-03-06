import string

import pandas as pd

import logging

from langdetect import detect

from src.features.videos import length_description, description_classifier
import src.util.config as config

def detect_lang(text):
    try:
        return detect(text)
    except Exception:
        return 'no_language_detected'

def remove_ponctuation(text):
    if text is not None and isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation)).lower()
    else:
        None


if __name__ == '__main__':
    c = config.Config()

    logging.getLogger().setLevel(logging.INFO)
    data = pd.read_csv(c.data_dir + c.raw_data + c.videos_file)

    #Drop duplicates
    data.drop_duplicates(subset='video_id', inplace=True, keep = 'last')

    data = data[data.relevant]
    logging.info('Relevant videos selected!')

    # Description cleanning

    data['video_description'] = data['video_description'].apply(remove_ponctuation)
    logging.info('Punctuation removed!')

    # description classifier
    data['description_level'] = data['video_description'].apply(length_description).apply(description_classifier)

    # Selecting only description with more than 2 words
    data = data[data.description_level]
    logging.info('Description with more tha 2 words selected!')

    #Select only description in English

    logging.info('Classifying description language...')

    data['language'] = data['video_description'].apply(detect_lang)

    data = data[data['language'] == 'en']

    logging.info('Only description in english selected!')

    data.to_csv(c.data_dir + c.processed_data + "videos_processed.csv", index=False)

    logging.info('Videos preprocessed!')