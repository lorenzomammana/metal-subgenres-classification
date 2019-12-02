from collections import Counter
import re
import pandas as pd
from multiset import Multiset
import os


rgx = re.compile(r"[\[\]\"' \n]")  # data cleanup

if __name__ == '__main__':
    try:
        changer = pd.read_csv('darklyrics-tokens.csv')
        changer.to_csv('darklyrics-tokens-temp.csv', index=False, sep='|')
    except:
        print('Already converted')

    # load and pre-process the data
    counter = Counter()
    data = []
    with open('darklyrics-tokens-temp.csv', 'r', encoding='utf8') as o:
        o.readline()
        for line in o:
            parts = line.split('|')
            words_sep = str(parts[5:][0]).split(',')
            clean_parts = [re.sub(rgx, "", i) for i in words_sep]
            counter.update(clean_parts)

            ms = Multiset()
            for word in clean_parts:
                ms.add(word)

            data.append([parts[:5], ms])

    os.remove('darklyrics-tokens-temp.csv')
    print('first part')
    n = 5  # <- here set threshold for number of occurences
    common_words = Multiset()

    for item in counter.items():
        if item[1] >= n:
            # Il 100 serve perchè l'intersection prende il numero di parole minore nel multiset
            # Vogliamo che il numero minore sia il numero di token
            common_words.add(item[0], 100)

    print('second part')
    # process the data
    clean_data = []
    for s in data:
        cleaner = s[1].intersection(common_words)
        clean_data.append([s[0], cleaner])

    print('third part')

    output_data = []
    for s, ms in clean_data:
        tokens = []
        for item in ms.items():
            for i in range(0, item[1]):
                tokens.append(item[0])

        output_data.append(s + [tokens])

    df = pd.DataFrame(output_data, columns=['band', 'album', 'year', 'song', 'genre', 'tokens'])
    df.to_csv('darklyrics-proc-tokens.csv', index=False)
