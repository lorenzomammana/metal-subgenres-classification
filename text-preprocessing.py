import pandas as pd
from preprocessing import RepeatReplacer

replacer = RepeatReplacer()


def remove_repetitions(x):
    output = []

    for token in x:
        check = replacer.replace(token)

        if token == check:
            output.append(token)
        else:
            output.append(replacer.replace_with_wordnet(token))

    return output


# Bisogna vedere se è possibile ottimizzare
# Anche il global è osceno
def remove_non_frequent(x):
    global frequentwords
    output = []

    for token in x:
        if token in frequentwords:
            output.append(token)

    return output


darklyrics = pd.read_csv('darklyrics-token.csv',
                         converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", "),
                                     'genre': lambda x: x.strip("[]").replace("'", "").split(", ")})

print("Loaded lyrics")

# Rimuove i token con lettere multiple tipo aaaarggghhh -> argh
darklyrics['tokens'] = darklyrics.apply(lambda x: remove_repetitions(x['tokens']), axis=1)


# Trovo le parole con almeno 5 occorrenze nell'intero dataset
# Di base sono 140k parole singole, quasi come l'intera lingua italiana
# Troppe per addestrare i modelli
allwords = [word for tokens in darklyrics['tokens'] for word in tokens]
allwords = pd.DataFrame(allwords, columns=['word'])

more5 = allwords[allwords.groupby("word")["word"].transform('size') >= 5]
more5 = set(more5['word'])
frequentwords = [token.strip() for token in more5]
frequentwords.sort()

# Tengo solo le parole più frequenti
# TODO testare questa cosa, ci mette tanto
darklyrics['tokens'] = darklyrics.apply(lambda x: remove_non_frequent(x['tokens']), axis=1)

darklyrics.to_csv('darklyrics-proc-tokens.csv', index=False)
