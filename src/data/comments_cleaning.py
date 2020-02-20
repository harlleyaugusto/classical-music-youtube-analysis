import string

import pandas as pd

import logging

from langdetect import detect

import spam_detection
from src.features.comments import length_description, description_classifier


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
    logging.getLogger().setLevel(logging.INFO)
    data = pd.read_csv("data/comments.csv", engine = 'python')

    # Drop duplicates
    data.drop_duplicates(subset='cid', inplace=True, keep='last')

    # Description cleanning
    data['text'] = data['text'].apply(remove_ponctuation)
    logging.info('Punctuation removed!')

    # description classifier
    data['text_level'] = data['text'].apply(length_description).apply(description_classifier)

    # Selecting only comments with more than 2 words
    data = data[data.text_level]
    logging.info('Text with more than 3 words selected!')

    # Select only description in English

    logging.info('Classifying text language...')

    data['language'] = data['text'].apply(detect_lang)

    data = data[data['language'] == 'en']

    logging.info('Only text in english selected!')

    logging.info('Spam filtering...')
    data['spam'] = spam_detection.classifier(data['text'])

    data = data[data['spam'] == 0]

    logging.info('Done!')

    data.to_csv("data/comments_processed.csv", index=False)
    data = pd.read_csv("data/comments_processed.csv", engine='python')

    logging.info('Comments preprocessed!')
