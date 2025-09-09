# Keras Seuential Model -> Sept 8th, 2025
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-1] # select all columns except for the first & last
y = data['Label'] # target column

# sequential model
model = tf.keras.Sequential([
    tf.keras.Input(shape=(x.shape[1],), name="inputs"),
    tf.keras.layers.Dense(1, activation="sigmoid", name="denseLayer"),
], name="sequentialModel")
model.compile(optimizer=RMSprop(learning_rate=0.001), loss="binary_crossentropy", metrics=["accuracy"])
model.fit(x, y, epochs=100, batch_size=32, validation_split=0.2)

# check performance
loss, accuracy = model.evaluate(x, y, verbose=0)

print(f'Test Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')

filename = 'sequentialModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
