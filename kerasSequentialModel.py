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
from keras.layers import Embedding, Flatten, Dense

data = pd.read_csv('urldata.csv')

x = data.iloc[:, 1:-1] # select all columns except for the first & last
y = data['Label'] # target column

# sequential model
vocab_size = 10000  # Expected by the model
embedding_dim = 16  # Received by the model

model = Sequential([
    Embedding(vocab_size, embedding_dim),
    Flatten(),
    Dense(128, activation='relu', input_shape=(len(y),)),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid') # Single output neuron with sigmoid activation
])

model.compile(optimizer=Nadam(), loss="binary_crossentropy", metrics=["accuracy"])
model.fit(x, y, epochs=100, batch_size=32, validation_split=0.2)

# check performance
loss, accuracy = model.evaluate(x, y, verbose=0)

print(f'Test Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')

filename = 'sequentialModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
