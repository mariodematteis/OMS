import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path
import csv

from algorithms.TrendFinder import DownloadData

def csvwriter(writer_, dateTime, openPrice, closePrice, highPrice, lowPrice, bbTop, bbMid, bbBottom, RSI, stochastic, ADX, CCI, DMI, momentumK, MACD, signal, stddev, sma7, sma10, sma20, sma50, sma100):
    rows = [dateTime, f'{openPrice:.5f}', f'{closePrice:.5f}', f'{highPrice:.5f}', f'{lowPrice:.5f}', f'{bbTop:.5f}', f'{bbMid:.5f}', f'{bbBottom:.5f}', f'{RSI:.6f}', f'{stochastic:.12f}', f'{ADX:.5f}', f'{CCI:.5f}', f'{DMI:.5f}', f'{momentumK:.12f}', f'{MACD:.12f}', f'{signal:.12f}', f'{stddev:.12f}', f'{sma7:.6f}', f'{sma10:.6f}', f'{sma20:.6f}', f'{sma50:.6f}', f'{sma100:.6f}']
    writer_.writerow(rows)

filename = "data/analysis.csv"

if not os.path.isfile(filename):
    dataset = DownloadData()
    with open(filename, mode="w") as csv_file:
        fieldnames = ['DATETIME', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'BB_TOP', 'BB_MID', 'BB_BOTTOM', 'RSI', 'STOCHASTIC', 'ADX', 'CCI', 'DMI', 'MOMENTUM_K', 'MACD', 'SIGNAL', 'STDDEV', 'SMA7', 'SMA10', 'SMA20', 'SMA50', 'SMA100']
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        for counter in range(0, len(dataset[0])):
            csvwriter(writer, dataset[0][counter], dataset[1][counter], dataset[2][counter], dataset[3][counter], dataset[4][counter], dataset[5][counter], dataset[6][counter], dataset[7][counter], dataset[8][counter], dataset[9][counter], dataset[10][counter], dataset[11][counter], dataset[12][counter], dataset[13][counter], dataset[14][counter], dataset[15][counter], dataset[16][counter], dataset[17][counter], dataset[18][counter], dataset[19][counter], dataset[20][counter], dataset[21][counter])

data_ = pd.read_csv(filename)
index1 = data_[data_["DATETIME"] == "10/05/2021, 00:00:00"].index[0]
index2 = data_[data_["DATETIME"] == "17/05/2021, 00:00:00"].index[0]
raw_data = data_[index1:index2]

from strategies.Piranha import slopeCalculator

arr = slopeCalculator(raw_data["SMA50"])
fig, ax = plt.subplots()
raw_data["SLOPE"] = arr
print(raw_data.head())

print(arr)

'''for index in range(len(raw_data.index)):
    if raw_data.iloc[index]["SLOPE"] > 1.1:
        print(raw_data.iloc[index])'''

arr_entrypoint = []
arr_tp = []
arr_sl = []



for index in range(len(raw_data.index)):
    if raw_data.iloc[index]['BB_BOTTOM'] > raw_data.iloc[index]['CLOSE']:
        if not (abs(raw_data.iloc[index+1]["SLOPE"] - raw_data.iloc[index]["SLOPE"]) > 0.01):
            arr_entrypoint.append(raw_data.iloc[index + 1]['OPEN'])
            arr_tp.append(raw_data.iloc[index + 1]['OPEN'] + 0.0005)
            arr_sl.append(raw_data.iloc[index + 1]['OPEN'] - 0.001)
        else:
            arr_entrypoint.append(None)
            arr_tp.append(None)
            arr_sl.append(None)
    else:
        arr_entrypoint.append(None)
        arr_tp.append(None)
        arr_sl.append(None)

raw_data["EP"] = arr_entrypoint
raw_data["TP"] = arr_tp
raw_data["SL"] = arr_sl

print(raw_data.head())

ax.plot(raw_data["CLOSE"], color="black")
ax.plot(raw_data["EP"], "*", color="blue")
ax.plot(raw_data["TP"], "o", color="green")
ax.plot(raw_data["SL"], "*", color="red")
#ax.plot(raw_data.index, raw_data["SLOPE"])
plt.xticks(rotation='vertical')
plt.show()

'''result1 = 0
result2 = 0
result3 = 0

print(raw_data)

arr = np.array(raw_data["ADX"])
mean = arr.mean()
print(mean)

for index in range(len(raw_data.index)):
    result1 = raw_data.iloc[index]["CLOSE"]
    #print(raw_data.iloc[index].name)
    if (raw_data.iloc[index].name + 5) < raw_data.iloc[-1].name:
        result2 = raw_data.iloc[index + 2]["CLOSE"]
        result3 = raw_data.iloc[index + 4]["CLOSE"]
    else:
        break

    if result1 > result2:
        if result2 > result3:
            if abs(result3-result1) < mean:
                raw_data.drop(raw_data.iloc[index].name, inplace=True)

data = raw_data
print(data)

subcond1 = data['BB_TOP'] < data['CLOSE']
subcond2 = data['CCI'] > 25
subcond3 = data["STOCHASTIC"] > 75
subcond4 = (data["MACD"] > data["SIGNAL"]) > 0
subcond5 = data["MOMENTUM_K"] > 35
cond1 = data[subcond1 & subcond2 & subcond3 & subcond4 & subcond5]
fig, ax = plt.subplots()
print(cond1)
ax.plot(data.index, data["CLOSE"], color="teal")
ax.plot(cond1.index, cond1["CLOSE"], 'o', color="red", markersize=5)
plt.show()'''
'''plt.plot(data["CLOSE"])
plt.plot(cond1["CLOSE"], color="red")
plt.title("EUR/USD (04/01/2021, 00:00:00 - 05/05/2021, 00:00:00)")
plt.show()
cond1 = data['BB_TOP' < 'BB_CLOSE']'''