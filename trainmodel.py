from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score
from llda import LLDAClassifier
import pandas as pd
from gensim import corpora


if __name__ == '__main__':
    darklyrics = pd.read_csv('darklyrics-proc-tokens.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", "),
                                         'genre': lambda x: x.strip("[]").replace("'", "").split(", ")})

    documents = darklyrics['tokens']
    dictionary = corpora.Dictionary(documents)
    corpus = documents.apply(lambda x: dictionary.doc2bow(x))
    labels = darklyrics.apply(lambda x: set(x['genre']), axis=1)

    X_train, X_test, y_train, y_test = train_test_split(corpus, labels, test_size=0.2, random_state=0)

    mlb = MultiLabelBinarizer(classes=['Heavy Metal', 'Thrash Metal', 'Power Metal',
                                       'Folk Metal', 'Progressive Metal', 'Death Metal',
                                       'Doom Metal', 'Black Metal', 'Rock'])
    y_train = [each for each in y_train]
    y_train = mlb.fit_transform(y_train)

    llda = LLDAClassifier(alpha=0.5 / y_train.shape[1], maxiter=100)
    llda.fit(X_train, y_train)
    result = llda.predict(X_test)
    y_test = mlb.fit_transform([each for each in y_test])

    score_macro = f1_score(y_test, result, average="macro")
    score_micro = f1_score(y_test, result, average="micro")
    print("F1_macro:{0}, F1_micro:{1}".format(score_macro, score_micro))

