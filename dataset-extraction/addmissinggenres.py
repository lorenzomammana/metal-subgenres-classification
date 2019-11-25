import pandas as pd
import math
import Levenshtein

darklyrics = pd.read_csv('darklyrics-lang.csv')

newgenres = pd.read_csv('manewgenres.csv',
                        converters={'albums': lambda x: x.strip("[]").replace("'", "").split(",")})


def findmatch(x):
    band = x['band']
    albums = [item.lower() for item in x['albums']]
    genre = x['genre']

    matchalbum = set(darklyrics[darklyrics['band'] == band]['album'])

    cont = 0

    for album in matchalbum:
        distances = [Levenshtein.distance(item, album.lower()) for item in albums]
        if min(distances) <= 2:
            cont += 1

    if cont >= math.ceil(len(matchalbum) / 2):
        darklyrics.loc[darklyrics['band'] == band, 'genre'] = genre


print(darklyrics['genre'].value_counts()[0])

newgenres.apply(lambda x: findmatch(x), axis=1)

print(darklyrics['genre'].value_counts()[0])

darklyrics.to_csv('darklyrics-lang2.csv', index=False)
