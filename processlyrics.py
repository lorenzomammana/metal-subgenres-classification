from functools import reduce

import pandas as pd
import numpy as np
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re


def _removeNonAscii(s):
    return "".join(i for i in s if ord(i) < 128)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", " is ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text


def tokenizer(text):
    text = clean_text(text)
    tokens = [word_tokenize(sent) for sent in sent_tokenize(text)]

    if not tokens:
        return ["error"]

    tokens = list(reduce(lambda x, y: x + y, tokens))
    tokens = list(filter(lambda token: token not in (stop + list(punctuation)), tokens))
    return tokens


lyrics = pd.read_csv('lyrics.csv', sep=',')

missing_values = np.sum(lyrics.isnull())

print("Numero di attributi mancanti")
print(missing_values)
# Rimuovo tutte le righe con attributi mancanti
lyrics = lyrics.dropna()

# Controllo l'esistenza di duplicati

print("\nNumero di duplicati: ", np.sum(lyrics.duplicated(['song', 'artist'])))

# Rimuovo le stopwords
stop = stopwords.words('english') + list(punctuation)

lyrics['lyrics'] = lyrics['lyrics'].map(lambda x: tokenizer(x))

lyrics.to_csv('lyrics-tokenize.csv')
