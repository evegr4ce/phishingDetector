# GradientBoostingClassifier -> Sept 8th, 2025 (0.804 accuracy)
# Utility
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

# Model Creation
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import TargetEncoder
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline

data = pd.read_csv('urldata.csv')

x = data.iloc[:, 1:-2]
y = data['Label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42, shuffle=True)

model = make_pipeline(
        TargetEncoder(),
        GradientBoostingClassifier(n_estimators=100, learning_rate=0.5, random_state=1),
    )
model.fit(x_train,y_train)

accuracy = model.score(x_test, y_test)
print(f"Accuracy: {accuracy}")

filename = 'gradientModel.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)
