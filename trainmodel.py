import labeled_lda as llda
import pandas as pd
import pickle

# TODO questo è tutto da fare ancora


def gen_lda_tuple(token, genre):
    return " ".join(token), [genre]


darklyrics = pd.read_csv('darklyrics-token.csv',
                         converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(",")})

print("Loaded lyrics")

dataset = darklyrics.apply(lambda x: gen_lda_tuple(x['lemmatokens'], x['genre']), axis=1)

print("Constructed dataset")

llda_model = llda.LldaModel(labeled_documents=dataset, alpha_vector='50_div_K')

print("Constructed model")

while True:
    print("iteration %s sampling..." % (llda_model.iteration + 1))
    llda_model.training(1)
    print("after iteration: %s, perplexity: %s" % (llda_model.iteration, llda_model.perplexity()))
    print("delta beta: %s" % llda_model.delta_beta)
    if llda_model.is_convergent(method="beta", delta=0.01):
        break

with open('ldamodel.pickle', 'wb') as f:
    pickle.dump(llda_model, f)
