# Linear Regression Model -> Sept 8th, 2025 (0.804 accuracy)
# Utility
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

# Model Creation
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-2]
y = data['Label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.99, random_state=42)

model = MLPClassifier(activation='tanh', max_iter=10000)
model.fit(x_train,y_train)

preds = model.predict(x_test)

accuracy = accuracy_score(y_test, preds)
print(f"Accuracy: {accuracy}")

filename = 'mlpModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
