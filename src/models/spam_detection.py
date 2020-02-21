import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
from sklearn.ensemble import RandomForestClassifier
import src.util.config as config
import math

def load_data():
    c = config.Config()
    train_data = []
    diretory = c.data_dir + c.external_data + 'spam_detection/'
    data_files = [diretory + 'Youtube01-Psy.csv',diretory + 'Youtube02-KatyPerry.csv',diretory + 'Youtube03-LMFAO.csv',diretory + 'Youtube04-Eminem.csv',diretory + 'Youtube05-Shakira.csv']
    for file in data_files:
        data = pd.read_csv(file)
        train_data.append(data)

    train_data.append(pd.read_csv(diretory + 'SMSSpamCollection.csv', engine = 'python'))
    train_data = pd.concat(train_data)

    return train_data

## Function which drops the given features from the given dataframe
def drop_fectures(features, data):
    data.drop(features, axis=1,inplace=True)

def process_content(content):
    if (content is not None and isinstance(content, str)) and (content is not None):
        return " ".join(re.findall("[A-Za-z]+",content.lower()))
    else:
        None

def classifier(data):
    train_data = load_data()
    drop_fectures(['COMMENT_ID', 'AUTHOR', 'DATE'], train_data)
    train_data['processed_content'] = train_data['CONTENT'].apply(process_content)
    drop_fectures(['CONTENT'], train_data)

    x_train, x_test, y_train, y_test = train_test_split(train_data['processed_content'], train_data['CLASS'],
                                                        test_size=0.2, random_state=57)

    count_vect = CountVectorizer(stop_words='english')
    x_train_counts = count_vect.fit_transform(x_train)

    tranformer = TfidfTransformer()
    x_train_tfidf = tranformer.fit_transform(x_train_counts)

    model = RandomForestClassifier()
    model.fit(x_train_tfidf, y_train)

    #TODO: verify it!!!
    comment_counts = count_vect.transform(data.apply(process_content))
    comment_tfidf = tranformer.transform(comment_counts)

    predictions = model.predict(comment_tfidf)

    return list(predictions)

if __name__ == '__main__':
    train_data = load_data()
    drop_fectures(['COMMENT_ID', 'AUTHOR', 'DATE'], train_data)
    train_data['processed_content'] = train_data['CONTENT'].apply(process_content)
    drop_fectures(['CONTENT'], train_data)

    x_train, x_test, y_train, y_test = train_test_split(train_data['processed_content'], train_data['CLASS'],
                                                        test_size=0.2, random_state=57)

    count_vect = CountVectorizer(stop_words='english')
    x_train_counts = count_vect.fit_transform(x_train)

    tranformer = TfidfTransformer()
    x_train_tfidf = tranformer.fit_transform(x_train_counts)

    x_test_counts = count_vect.transform(x_test)
    x_test_tfidf = tranformer.transform(x_test_counts)

    model = LogisticRegression()
    model.fit(x_train_tfidf, y_train)

    predictions = model.predict(x_test_tfidf)

    print(classification_report(y_test,predictions))

    model = RandomForestClassifier()
    model.fit(x_train_tfidf, y_train)

    predictions = model.predict(x_test_tfidf)

    print(classification_report(y_test, predictions))

    #data = pd.read_csv("data/comments_processed.csv", engine = 'python')
    #comment_counts = count_vect.transform(data['text'].apply(process_content).dropna())
    #comment_tfidf = tranformer.transform(comment_counts)
    #predictions = model.predict(comment_tfidf)


    #classifier(data['text'].apply(process_content).dropna())


    #http://www.dt.fee.unicamp.br/~tiago//youtubespamcollection/