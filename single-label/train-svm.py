from sklearn.svm import LinearSVC
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def train(X, labels):
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=0)

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    clf = LinearSVC(class_weight='balanced')

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    score_macro = f1_score(y_test, y_pred, average="macro")
    score_micro = f1_score(y_test, y_pred, average="micro")
    print("F1_macro:{0}, F1_micro:{1}".format(score_macro, score_micro))
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    darklyrics = pd.read_csv('../darklyrics-proc-tokens-single.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", ")})

    corpus = darklyrics.apply(lambda x: " ".join(x['tokens']), axis=1)

    # TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics['genre']

    train(X, labels)

    # TF
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics['genre']

    train(X, labels)

    # Binary
    vectorizer = CountVectorizer(binary=True)
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics['genre']

    train(X, labels)