from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, OneHotEncoder
from sklearn.metrics import f1_score, classification_report, hamming_loss, accuracy_score
import pandas as pd
from gensim import corpora
import sys
sys.path.append("..")
import numpy as np
from llda import LLDAClassifier


if __name__ == '__main__':
    darklyrics = pd.read_csv('../darklyrics-proc-tokens-single.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", ")})

    documents = darklyrics['tokens']
    dictionary = corpora.Dictionary(documents)
    corpus = documents.apply(lambda x: dictionary.doc2bow(x))
    labels = darklyrics['genre']

    X_train, X_test, y_train, y_test = train_test_split(corpus, labels, test_size=0.2, random_state=0)

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    onehot = OneHotEncoder(sparse=False)
    y_train = onehot.fit_transform(y_train.reshape(len(y_train), 1))
    y_train = y_train.astype(int)
    y_test_oh = onehot.transform(y_test.reshape(len(y_test), 1))
    y_test_oh = y_test_oh.astype(int)

    llda = LLDAClassifier(alpha=0.1, beta=0.1, maxiter=100)
    llda.fit(X_train, y_train)
    preds = llda.predict(X_test)

    print(classification_report(y_test_oh, preds))
    print(hamming_loss(y_test_oh, preds))
    print(accuracy_score(y_test_oh, preds))

