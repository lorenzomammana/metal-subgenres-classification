from sklearn import svm
import pandas as pd
from sklearn import tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np


def fit(s):
    darklyrics = pd.read_csv('darklyrics-proc-tokens-single.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", ")})

    corpus = darklyrics.apply(lambda x: " ".join(x['tokens']), axis=1)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    X = X.todense()
    X = np.array(X)
    labels = darklyrics['genre']

    print('Fase Split')
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=0)

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    if s == "tree":
        clf = tree.DecisionTreeClassifier()
    elif s == "svm":
        clf = svm.SVC()
    elif s == "lda":
        clf = LinearDiscriminantAnalysis()
    else:
        print("Choose among 'svm', 'tree', 'lda'")
        return 0

    print('Fitting')
    clf.fit(X_train, y_train)

    print('Predict')
    y_pred = clf.predict(X_test)

    print('Result')
    score_macro = f1_score(y_test, y_pred, average="macro")
    score_micro = f1_score(y_test, y_pred, average="micro")
    print("F1_macro:{0}, F1_micro:{1}".format(score_macro, score_micro))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    #clf = MultiOutputClassifier(SVC()).fit(X_train, y_train)


if __name__ == '__main__':
    fit("tree")
    fit("svm")
    fit("lda")
