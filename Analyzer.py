from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import datetime
import io
import json
import math
from decimal import *

import backtrader as bt
import matplotlib.pyplot as plt
import numpy
import numpy as np
import sympy as sym
from numpy import exp, log
from pync import Notifier
from scipy import stats

from algorithms.TrendFinder import TrendFinder

csv_filename = "analysis_2.csv"

stockkwargs = dict(
    timeframe=bt.TimeFrame.Ticks,
    what='BID',
    fromdate=datetime.datetime(2021, 4, 28),
    todate=datetime.datetime(2021, 4, 30),
    historical=True,
    qcheck=0.5,
    latethrough=False,
    tradename=None,
    tz="Europe/Rome"
)



def HMHugeMovement(data, stddev):
    vectorsValue = len(data)
    counter = vectorsValue - 1
    for price in range(1, vectorsValue):
        difference = data[counter] - data[counter - 1]
        value = abs(Decimal(f'{difference:.5f}'))
        if value != 0:
            print(value, "   LN: ", log(float(value)), "STDDEV: ",
                  f'{10 ** exp(stddev[counter] ** 2):.10f}')

        else:
            print(value, "   LN: NOT AVAILABLE", "STDDEV: ", f'{10 ** exp(stddev[counter] ** 2):.10f}') # noqa E507

        counter -= 1


def DerivativeOfStandardDeviation(data):
    return str(sym.diff(float(data)))


class analyzer(bt.Strategy):
    params = (
        ('rsi_period', 7),
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('BBandsperiod', 20)
    )

    def __init__(self):
        self.csv_script = io.StringIO()
        self.csv_writer = csv.writer(self.csv_script, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) #noqa E507

        self.name = self.data._name
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.params.macd1,
                                       period_me2=self.params.macd2,
                                       period_signal=self.params.macdsig)
        self.bband = bt.indicators.BBands(self.data, period=self.params.BBandsperiod)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.stochastic_slow = bt.indicators.Stochastic(self.data, upperband=75.0, lowerband=25.0)
        self.momentumK = bt.indicators.Momentum(self.stochastic_slow.percK, period=18)
        self.momentumD = bt.indicators.Momentum(self.stochastic_slow.percD, period=18)
        self.momentumRSI = bt.indicators.Momentum(self.rsi, period=18)
        self.parabolic_sar = bt.indicators.ParabolicSAR(self.data)
        self.standard_deviation = bt.indicators.StandardDeviation(self.data)
        self.standard_deviation_5 = bt.indicators.StdDev(period=5)
        self.m5_available = False
        self.counter = 0
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0
        self.m5 = 0
        self.standard_deviation_plot = []
        self.standard_deviation_derivated_plot = []
        self.x = []
        self.y = []
        self.close_prices = []
        self.stddev_5 = []

    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:  # the data has switched to live data
            print("ON AIR...")
            pass
        elif status == data.DELAYED:
            print("LOADING LIVE...")
            pass
        elif status == data.NOTSUBSCRIBED:
            print("NOTSUBSCRIBED")
            pass
        elif status == data.CONNBROKEN:
            print("CONNBROKEN")
            pass
        elif status == data.DISCONNECTED:
            trendFinder = TrendFinder(self.close_prices)

            #LNListGenerator(self.close_prices)
            #HMHugeMovement(self.close_prices, self.stddev_5)
            with open("analysis_2.csv", mode="w") as csv_file:
                csv_file.write(self.csv_script.getvalue())

            # mymodel = numpy.poly1d(numpy.polyfit(self.x, self.y, 3))

            # myline = numpy.linspace(1, 22, 100)
            # plt.subplot(self.standard_deviation_derivated_plot)
            # plt.scatter(self.x, self.y)
            # plt.plot(myline, mymodel(myline))
            # plt.show()
            #result = appendValues(listLN)
            '''if result["MESSAGE"] == "NONE":
                print("NO TRENDING")
            else:
                print("TRENDING")'''
            print("DISCONNECTED")
            pass
        elif status == data.CONNECTED:
            print("CONNECTED")
            pass

    def logdata(self):
        self.m5 = f'{self.momentumK[0]:.10f}'
        _candleInfo = {
            "FINANCIAL INSTRUMENT": self.name,
            "DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"),
            "MASSIMO": self.data.high[0],
            "APERTURA": self.data.open[0],
            "CHIUSURA": self.data.close[0],
            "MINIMO": self.data.low[0],
            "RSI": self.rsi[0],
            "MOMENTUM %D": self.momentumD[0],
            "MOMENTUM %K": self.momentumK[0],
            "MOMENTUM RSI": self.momentumRSI[0],
            "STOCHASTIC (SLOW)": self.stochastic_slow.percK[0],
            "PARABOLIC SAR": self.parabolic_sar[0],
            "STANDARD DEVIATION": self.standard_deviation[0],
            "STANDARD DEVIATION 5": f'{self.standard_deviation_5.stddev[0]:.10f}',
        }
        _candleInfo = {"DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"),
                       "DERIVATIVE": DerivativeOfStandardDeviation(f'{self.standard_deviation_5.stddev[0]:.10f}'), # noqa E507
                       "CLOSE": self.data.close[0]}

        if self.m5_available:
            self.m1 = self.m2
            self.m2 = self.m3
            self.m3 = self.m4
            self.m4 = self.m5
        else:
            _candleInfo["DERIVATIVE"] = "STILL NOT AVAILABLE"

        print(json.dumps(_candleInfo))

    def next(self):
        self.close_prices.append([self.name, self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"), self.data.close[0]])
        self.stddev_5.append(Decimal(f'{self.standard_deviation_5.stddev[0]:.10f}'))

        self.counter += 1
        if self.counter == 1:
            self.m1 = f'{self.momentumK[0]:.10f}'
        elif self.counter == 2:
            self.m2 = f'{self.momentumK[0]:.10f}'
        elif self.counter == 3:
            self.m3 = f'{self.momentumK[0]:.10f}'
        elif self.counter == 4:
            self.m4 = f'{self.momentumK[0]:.10f}'
        elif self.counter == 5:
            self.m5_available = True
        self.logdata()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    ibstore = bt.stores.IBStore(host="127.0.0.1", port=7497)
    data = ibstore.getdata(dataname="EUR.USD-CASH-IDEALPRO", **stockkwargs)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)
    cerebro.addstrategy(analyzer)
    cerebro.run()
