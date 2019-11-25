import pandas as pd
import re
import numpy as np

darklyrics = pd.read_csv('darklyrics-lang2.csv')

yeargenre = []


def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))

def removesquarebr(x):
    output = re.sub(r'\[[^]]*\]', "", x)

    return output.strip()


def processgenres(band, x):
    x = x.replace("|", "/")
    x = x.replace("Metal", "")
    x = re.sub(r'\([^]]*\)', "", x)
    x = x.split(" with")[0]

    output = []

    split = x.split("/")

    for s in split:
        if s == "MISSING":
            output.append(s)
        elif "Rock" in s or "Punk" in s or "Blues" in s:
            output.append("Rock")
        elif "Black" in s or "Atmospheric" in s:
            output.append("Black Metal")
        elif "Doom" in s or "Gothic" in s or "Ambient" in s or "Sludge" in s:
            output.append("Doom Metal")
        elif "Death" in s or "core" in s or "Brutal" in s or "Extreme" in s or "EBM" in s:
            output.append("Death Metal")
        elif "Progressive" in s or "Avant-garde" in s or "Jazz" in s:
            output.append("Progressive Metal")
        elif "Folk" in s or "Celtic" in s or "Viking" in s or "Pagan" in s or "Medieval" in s:
            output.append("Folk Metal")
        elif "Power" in s or "Symphonic" in s or "Epic" in s or "Classical" in s or "Shred" in s:
            output.append("Power Metal")
        elif "Thrash" in s or "Speed" in s or "Groove" in s or "Stoner" in s:
            output.append("Thrash Metal")
        elif "Heavy" in s or "Nu" in s or "Glam" in s or "Industrial" in s or "Electronic" in s or "Alternative" in s \
                or "NWOBHM" in s or "Various" in s or "New Wave":
            output.append("Heavy Metal")
        else:
            output.append(s)

    return output


genreorder = {'Heavy Metal': 0,
              'Thrash Metal': 1,
              'Power Metal': 2,
              'Folk Metal': 3,
              'Progressive Metal': 4,
              'Death Metal': 5,
              'Doom Metal': 6,
              'Black Metal': 7,
              'Rock': 8}


def singularizegenre(x):
    if len(x) != 1:
        x = mode(x)

    if len(x) != 1:
        maximum = -1
        maxgenre = ""

        for genre in x:
            if genreorder.get(genre) > maximum:
                maxgenre = genre
                maximum = genreorder.get(genre)

        return maxgenre

    return x[0]


if __name__ == '__main__':
    # Rimuovo le canzoni senza liriche
    darklyrics = darklyrics.dropna()

    # Rimuovo le annotazioni nelle quadre
    darklyrics['lyrics'] = darklyrics.apply(lambda x: removesquarebr(x['lyrics']), axis=1)

    # Rimuovo possibili strumentali
    darklyrics = darklyrics[darklyrics['lyrics'] != '']

    print(darklyrics['lang'].value_counts())

    darklyrics = darklyrics[darklyrics['lang'] == 'en']

    darklyrics['genre'] = darklyrics.apply(lambda x: processgenres(x['band'], x['genre']), axis=1)

    darklyrics = darklyrics[darklyrics.apply(lambda x: 'MISSING' not in x['genre'], axis=1)]

    darklyrics['genre'] = darklyrics.apply(lambda x: singularizegenre(x['genre']), axis=1)

    darklyrics.to_csv('darklyrics-en.csv', index=False)
