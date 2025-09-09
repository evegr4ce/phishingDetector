# Keras Seuential Model -> Sept 8th, 2025
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-1]
y = data['Label']

model = tf.keras.Sequential([
    tf.keras.Input(shape=(1,), name="my_input"),
    tf.keras.layers.Dense(1, activation="sigmoid", name="my_dense"),
], name="my_sequential")
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
model.fit(x,y)

preds = model.predict(x)
print(preds)

correct = y == preds

print("Accuracy", np.average(correct))
