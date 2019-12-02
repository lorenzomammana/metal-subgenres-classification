import pandas as pd

from preprocessing import removesquarebr, processgenres, fix_wrong_unicode, tokenize, lemmatize, remove_repetitions

darklyrics = pd.read_csv('darklyrics-lang.csv')

if __name__ == '__main__':
    # Rimuovo le canzoni senza liriche
    darklyrics = darklyrics.dropna()

    # Rimuovo le annotazioni nelle quadre
    darklyrics['lyrics'] = darklyrics.apply(lambda x: removesquarebr(x['lyrics']), axis=1)

    # Rimuovo possibili strumentali
    darklyrics = darklyrics[darklyrics['lyrics'] != '']

    # print(darklyrics['lang'].value_counts())

    # Rimuovo le canzoni non in inglese
    darklyrics = darklyrics[darklyrics['lang'] == 'en']

    darklyrics = darklyrics.drop('lang', axis=1)
    # Parso i generi, vedere funzione
    darklyrics['genre'] = darklyrics.apply(lambda x: processgenres(x['genre']), axis=1)

    # Rimuovo le canzoni con genere mancante
    darklyrics = darklyrics[darklyrics.apply(lambda x: 'MISSING' not in x['genre'], axis=1)]
    # generi = [lista for lista in darklyrics['genre'] if len(lista)>1]

    # Trasformo da multi-label a singola label, da valutare
    # darklyrics['genre'] = darklyrics.apply(lambda x: singularizegenre(x['genre']), axis=1)

    # Magia
    print("fix unicode")
    darklyrics['lyrics'] = darklyrics.apply(lambda x: fix_wrong_unicode(x['lyrics']), axis=1)

    # Pulizia dei token
    print("tokenize")
    darklyrics['tokens'] = darklyrics.apply(lambda x: tokenize(x['lyrics']), axis=1)

    print("remove repetitions")
    # Rimuove i token con lettere multiple tipo aaaarggghhh -> argh
    darklyrics['tokens'] = darklyrics.apply(lambda x: remove_repetitions(x['tokens']), axis=1)

    print("lemmatize")
    darklyrics['tokens'] = darklyrics.apply(lambda x: lemmatize(x['tokens']), axis=1)

    darklyrics = darklyrics.drop('lyrics', axis=1)

    darklyrics.to_csv('darklyrics-tokens.csv', index=False)
