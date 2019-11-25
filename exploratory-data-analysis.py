import re
import string
from collections import Counter
import pandas as pd
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from nltk.stem import LancasterStemmer

matplotlib.use('TkAgg')
stop = set(nltk.corpus.stopwords.words('english'))
lemmatizer = LancasterStemmer()


def tokenize(x):
    """
    sent_tokenize(): segment text into sentences
    word_tokenize(): break sentences into words
    """
    try:
        regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
        x = regex.sub(" ", x)  # remove punctuation

        tokens_ = [nltk.word_tokenize(s) for s in nltk.sent_tokenize(x)]
        tokens = []
        for token_by_sent in tokens_:
            tokens += token_by_sent
        tokens = list(filter(lambda t: t.lower() not in stop, tokens))
        filtered_tokens = [w for w in tokens if re.search('[a-zA-Z]', w)]
        filtered_tokens = [w.lower() for w in filtered_tokens if len(w) >= 3]

        return filtered_tokens

    except TypeError as e:
        print(x, e)


def lemmatize(x):
    out = []

    for word in x:
        out.append(lemmatizer.stem(word))

    return out


def generate_wordcloud(tup):
    wordcloud = WordCloud(width=1600, height=800, background_color='black',
                          max_words=50,
                          random_state=42).generate(str(tup).replace("'", ""))
    return wordcloud


darklyrics = pd.read_csv('darklyrics-en.csv')

genres = set(darklyrics['genre'].unique())

genre_lyrics = dict()
for genre in genres:
    text = " ".join(darklyrics.loc[darklyrics['genre'] == genre, 'lyrics'].values)
    genre_lyrics[genre] = tokenize(text)

for genre in genres:
    top100 = Counter(genre_lyrics[genre]).most_common(100)
    print(top100)
    # wordcloud = generate_wordcloud(top100)
    #
    # plt.figure(figsize=(20, 10))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.savefig(genre + ".png", bbox_inches='tight')

darklyrics['year'].value_counts().sort_index().plot(kind='bar')

genre_per_year = darklyrics.groupby(['year', 'genre'])['year'].count().unstack('genre').fillna(0)
genre_per_year.plot(kind='bar', stacked=True)

darklyrics['tokens'] = darklyrics.apply(lambda x: tokenize(x['lyrics']))
darklyrics['lemmatokens'] = darklyrics.apply(lambda x: lemmatize(x['tokens']), axis=1)

