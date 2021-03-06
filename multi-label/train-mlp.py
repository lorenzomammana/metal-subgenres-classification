from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, classification_report, accuracy_score, hamming_loss
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from tensorflow.keras import Sequential, Input
from tensorflow.keras import backend as K


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def train(X, labels):
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=0)

    mlb = MultiLabelBinarizer(classes=['Heavy Metal', 'Thrash Metal', 'Power Metal',
                                       'Folk Metal', 'Progressive Metal', 'Death Metal',
                                       'Doom Metal', 'Black Metal', 'Rock'])
    y_train = [each for each in y_train]
    y_train = mlb.fit_transform(y_train)
    y_test = [each for each in y_test]
    y_test = mlb.fit_transform(y_test)

    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=(1305,)))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(9, activation='sigmoid'))

    mcp_save = ModelCheckpoint('best_mlp.h5', save_best_only=True, monitor='val_f1_m', mode='max')
    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4, mode='min')
    EarlyStopping(monitor='val_loss', min_delta=0.001, patience=5, verbose=0, mode='min')

    opt = Adam(lr=0.01)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['acc', f1_m])

    model.fit(X_train, y_train, batch_size=64, epochs=50, verbose=2,
              validation_data=(X_test, y_test), callbacks=[mcp_save, reduce_lr_loss])

    model.load_weights('best_mlp.h5')

    preds = model.predict(X_test)
    preds[preds >= 0.5] = 1
    preds[preds < 0.5] = 0

    print(classification_report(y_test, preds))
    print(hamming_loss(y_test, preds))
    print(accuracy_score(y_test, preds))


if __name__ == '__main__':
    darklyrics = pd.read_csv('../darklyrics-proc-tokens.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", "),
                                         'genre': lambda x: x.strip("[]").replace("'", "").split(", ")})

    corpus = darklyrics.apply(lambda x: " ".join(x['tokens']), axis=1)
    # TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics.apply(lambda x: set(x['genre']), axis=1)

    train(X, labels)

    # TF
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics.apply(lambda x: set(x['genre']), axis=1)

    train(X, labels)

    # Binary
    vectorizer = CountVectorizer(binary=True)
    X = vectorizer.fit_transform(corpus)
    labels = darklyrics.apply(lambda x: set(x['genre']), axis=1)

    train(X, labels)
