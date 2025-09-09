# Keras Sequential Model -> Sept 8th, 2025
# Utility
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

# Model Creation
import tensorflow as tf
from keras.optimizers import RMSprop
from keras.optimizers import Nadam
from keras.models import Sequential
from keras.layers import Dense

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-1] # select all columns except for the first & last
y = data['Label'] # target column

# sequential model
model = tf.keras.Sequential([
    tf.keras.Input(shape=(x.shape[1],), name="inputs"),
    tf.keras.layers.Dense(1, activation="sigmoid", name="denseLayer"),
], name="sequentialModel")
model.compile(optimizer=Nadam(), loss="binary_crossentropy", metrics=["accuracy"])
model.fit(x, y, epochs=100, batch_size=32, validation_split=0.2)

# check performance
loss, accuracy = model.evaluate(x, y, verbose=0)

print(f'Test Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')

filename = 'sequentialModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
