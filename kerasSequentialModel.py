# Keras Seuential Model -> Sept 8th, 2025
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-1]
y = data['Label']

model = tf.keras.Sequential([
    tf.keras.Input(shape=(x.shape[1],), name="my_input"),
    tf.keras.layers.Dense(1, activation="sigmoid", name="my_dense"),
], name="my_sequential")
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["mae"])
model.fit(x, y, epochs=40, batch_size=32, validation_split=0.2)

preds = (model.predict(x) > 0.5).astype(int)
correct = (y == preds.flatten())

print("Accuracy:", np.mean(correct))

filename = 'sequentialModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
