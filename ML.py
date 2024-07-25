import pandas as pd
import numpy as np
import csv
import io
import os.path
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

from algorithms.TrendFinder import DownloadData

def csvwriter(writer_, dateTime, closePrice, RSI, stochastic, ADX, CCI, DMI, momentumK):
    rows = [dateTime, f'{closePrice:.5f}', f'{RSI:.6f}', f'{stochastic:.12f}', f'{ADX:.5f}', f'{CCI:.5f}', f'{DMI:.5f}', f'{momentumK:.12f}']
    writer_.writerow(rows)

filename = "data/analysisj.csv"

if not os.path.isfile(filename):
    dataset = DownloadData()
    with open(filename, mode="w") as csv_file:
        fieldnames = ['DATETIME', 'CLOSE', 'RSI', 'STOCHASTIC', 'ADX', 'CCI', 'DMI', 'MOMENTUM_K']
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        for counter in range(0, len(dataset[0])):
            csvwriter(writer, dataset[0][counter], dataset[1][counter], dataset[2][counter], dataset[3][counter], dataset[4][counter], dataset[5][counter], dataset[6][counter], dataset[7][counter])

dataset_csv = pd.read_csv(filename)

X = dataset_csv.iloc[:, 2:9].values
y = dataset_csv.iloc[:, 1].values

print(X)
print("ok")
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

'''sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)'''

regressor = RandomForestRegressor(n_estimators=500, random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict([y])

'''from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))'''

original_dataset = y.tolist()
forecasted = y.tolist()


for counter in range(0, len(y_pred)):
    forecasted.append(y_pred[counter])

print(y_pred)

plt.plot(forecasted)
plt.plot(original_dataset)
plt.show()