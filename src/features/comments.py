import pandas as pd
import string
from nltk import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
import nltk
import textstat

import src.util.config as config

def remove_ponctuation(text):
    if text is not None and isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    else:
        None

# Process text
def process_text(raw_text):
    raw_text = raw_text.replace('\ufeff', '')
    raw_text = remove_ponctuation(raw_text)
    token_text = word_tokenize(raw_text)
    return token_text


def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne


# Stanford NER tagger
def stanford_tagger(token_text, st):
    ne_tagged = st.tag(token_text)
    return (ne_tagged)

def nltk_tagger(token_text):
	tagged_words = nltk.pos_tag(token_text)
	ne_tagged = nltk.ne_chunk(tagged_words)
	return (ne_tagged)

# Tag tokens with standard NLP BIO tags
def bio_tagger(ne_tagged):
    bio_tagged = []
    prev_tag = "O"
    for token, tag in ne_tagged:
        if tag == "O":  # O
            bio_tagged.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged.append((token, "B-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged.append((token, "I-" + tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged.append((token, "B-" + tag))
            prev_tag = tag
    return bio_tagged


# Create tree
def stanford_tree(bio_tagged):
    tokens, ne_tags = zip(*bio_tagged)
    pos_tags = [pos for token, pos in pos_tag(tokens)]

    conlltags = [(token, pos, ne) for token, pos, ne in zip(tokens, pos_tags, ne_tags)]
    ne_tree = conlltags2tree(conlltags)
    return ne_tree


def stanford_main(raw_text, st):
    if raw_text is not None and isinstance(raw_text, str):
        return structure_ne(stanford_tree(bio_tagger(stanford_tagger(process_text(raw_text), st))))
    else:
        return None

def nltk_main(raw_text):

    if raw_text is not None and isinstance(raw_text, str):
        return structure_ne(nltk_tagger(process_text(raw_text)))
    else:
        return None

def format_readeable(lst):
    #print(lst)
    if (lst is not None):
        return ', '. join([i[0] for i in lst])

def length_description(text):
    if text is not None and isinstance(text, str):
        return word_tokenize(text).__len__()
    else:
        return 0

def description_classifier(len):
    if(len < 4):
        return False
    else:
        return True

if __name__ == '__main__':
    c = config.Config()
    data = pd.read_csv(c.data_dir + c.processed_data + "comments_processed.csv")

    authors = data.groupby('author').count()

    u = list(authors.index)
    c = list(authors.iloc[:, 0])

    #st = StanfordNERTagger(
    #    '/home/harlley/Projects/deliverableD4.2-2/venv/lib/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
    #    '/home/harlley/Projects/deliverableD4.2-2/venv/lib/stanford-ner-2018-10-16/stanford-ner.jar', encoding='utf-8')

    lst = data.iloc[:, 1].apply(nltk_main)

    #NEED TO BE CHECKED
    lst.apply(format_readeable)

    readability = data.iloc[:, 1].apply(remove_ponctuation)

    #MUST TO BE VERIFIED
    readability = readability.apply(lambda text: textstat.flesch_reading_ease(text) if (text is not None) else text)

    df = {'user_id': u, 'user_commments': c}
    df = pd.DataFrame(df)
    df.to_csv("data/u_comments.csv", index=False)

    df = {'user_id': list(data.author), 'comment': list(data.text), 'entity': list(lst), 'flesch_reading_ease':list(readability)}
    df = pd.DataFrame(df)

    df.to_csv("data/s_comments.csv", index=False)




