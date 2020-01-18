from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras import Sequential, Input
from tensorflow.keras import backend as K
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'


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


if __name__ == '__main__':
    darklyrics = pd.read_csv('../darklyrics-proc-tokens-single.csv',
                             converters={'tokens': lambda x: x.strip("[]").replace("'", "").split(", ")})

    corpus = darklyrics.apply(lambda x: " ".join(x['tokens']), axis=1)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    X = X.todense()
    X = np.array(X)
    labels = darklyrics['genre']

    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=0)

    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    onehot = OneHotEncoder(sparse=False)
    y_train = onehot.fit_transform(y_train.reshape(len(y_train), 1))
    y_test_oh = onehot.transform(y_test.reshape(len(y_test), 1))

    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=(1305,)))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(9, activation='softmax'))

    mcp_save = ModelCheckpoint('best_mlp.h5', save_best_only=True, monitor='val_f1_m', mode='max')
    reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, epsilon=1e-4, mode='min')

    opt = Adam(lr=0.01)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['acc', f1_m])

    model.fit(X_train, y_train, batch_size=64, epochs=50, verbose=2,
              validation_data=(X_test, y_test_oh), callbacks=[mcp_save, reduce_lr_loss])

    model.load_weights('best_mlp.h5')

    preds = model.predict(X_test)
    preds = np.argmax(preds, axis=1)

    print(classification_report(y_test, preds))
