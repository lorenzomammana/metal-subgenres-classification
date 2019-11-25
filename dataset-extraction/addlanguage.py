import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


def detectalsoerrors(x):
    global i
    print(i)
    i += 1
    try:
        return detect(x)
    except TypeError:
        return "MISSING"
    except LangDetectException:
        return "UNKNOWN"


i = 1
lyrics = pd.read_csv('darklyrics2.csv')
lyrics = lyrics.drop(['band', 'album', 'year', 'song', 'genre'], axis=1)
lyrics['lang'] = ""

lyrics['lang'] = lyrics.apply(lambda x: detectalsoerrors(x['lyrics']), axis=1)

lyrics = lyrics.drop(['lyrics'], axis=1)
lyrics.to_csv('languages.csv', index=False)
