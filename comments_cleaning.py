import string

import pandas as pd

import logging

from langdetect import detect

from comments import length_description, description_classifier


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
    data = pd.read_csv("data/comments.csv")
    v_data = pd.read_csv("data/videos.csv")

    # Description cleanning
    data['text'] = data['text'].apply(remove_ponctuation)
    logging.info('Punctuation removed!')

    # description classifier
    data['text_level'] = data['text'].apply(length_description).apply(description_classifier)

    # Selecting only description with more than 2 words
    data = data[data.text_level]
    logging.info('Text with more tha 2 words selected!')

    # Select only description in English

    logging.info('Classifying text language...')

    data['language'] = data['text'].apply(detect_lang)

    data = data[data['language'] == 'en']

    logging.info('Only text in english selected!')

    data.to_csv("data/comments_processed.csv", index=False)

    logging.info('Comments preprocessed!')
