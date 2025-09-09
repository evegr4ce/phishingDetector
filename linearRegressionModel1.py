# Linear Regression Model -> Sept 8th, 2025 (0.804 accuracy)

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

data = pd.read_csv('./DataFiles/urldata.csv')

x = data.iloc[:, 1:-1]
y = data['Label']

model = LogisticRegression(penalty='l2', max_iter=500, solver='newton-cg')
model.fit(x,y)

preds = model.predict(x)
print(preds)

correct = y == preds

print("Accuracy", np.average(correct))
