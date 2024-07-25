from __future__ import absolute_import, division, print_function, unicode_literals

import json

import backtrader as bt
import numpy as np
from pync import Notifier


def slopeCalculator(data):
    slopeArray = np.array([])
    for index in range(len(data.index)):
        if (index + 3) == len(data.index):
            break

        result = (data.iloc[index + 2] - data.iloc[index])/3
        slopeArray = np.append(slopeArray, result)

    slopeArray = np.append(slopeArray, 0)
    slopeArray = np.append(slopeArray, 0)
    slopeArray = np.append(slopeArray, 0)
    return np.e**(slopeArray*1000)

class strategy_nottofar(bt.Strategy):

    params = (
        ('BBandsperiod', 12),
        ('SMAPeriod_1', 7)
    )

    def __init__(self):
        self.delayed = True
        self.name = self.data._name
        self.bband = bt.indicators.BBands(self.data, period=self.params.BBandsperiod)


    def notify_data(self, data, status, *args, **kwargs):
        if status == data.LIVE:
            print("ON AIR...")
            print(type(data))
            self.delayed = False
            pass
        elif status == data.DELAYED:
            print("LOADING LIVE...")
            print(type(data))
            pass
        elif status == data.NOTSUBSCRIBED:
            print("NOTSUBSCRIBED")
            pass
        elif status == data.CONNBROKEN:
            print("CONNBROKEN")
            pass
        elif status == data.DISCONNECTED:
            print("DISCONNECTED")
            pass
        elif status == data.CONNECTED:
            print("CONNECTED")
            pass

    def logdata(self):
        _candleInfo = {
            "FINANCIAL INSTRUMENT": self.name,
            "DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"),
            "MASSIMO": self.data.high[0],
            "APERTURA": self.data.open[0],
            "CHIUSURA": self.data.close[0],
            "MINIMO": self.data.low[0],
            "ATR": round(self.atr[0], 5),
            "VOLUME" : self.data.volume[0],
        }

    def next(self):
        self.logdata()

        if not self.delayed:
            if self.macd.macd > self.macd.signal:

                if self.bband.lines.top <= self.data.close[0]:
                    # print("YOU COULD GO LONG")
                    if self.rsi > 70:
                        _candleInfo = {
                            "FINANCIAL INSTRUMENT": self.name,
                            "DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"), # noqa E507
                            "MASSIMO": self.data.high[0],
                            "APERTURA": float(format(self.data.open[0], '.6f')),
                            "CHIUSURA": float(format(self.data.close[0], '.6f')),
                            "MINIMO": float(format(self.data.low[0], '.6f')),
                            "ATR": round(self.atr[0], 5)
                        }
                        print("GO LONG!     - ", json.dumps(_candleInfo))
                        Notifier.notify(title="EUR/USD - 5 min time range",
                                        message="GO LONG!",
                                        open="https://live.trading212.com/")
            else:
                if self.bband.lines.bot >= self.data.close[0]:
                    if self.rsi < 30:
                        _candleInfo = {
                            "FINANCIAL INSTRUMENT": self.name,
                            "DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"), # noqa E507
                            "MASSIMO": self.data.high[0],
                            "APERTURA": self.data.open[0],
                            "CHIUSURA": self.data.close[0],
                            "MINIMO": self.data.low[0],
                            "ATR": round(self.atr[0], 5)
                        }
                        print("GO SHORT!    - ", json.dumps(_candleInfo))
                        Notifier.notify(title="EUR/USD - 5 min time range",
                                        message="GO SHORT!",
                                        open="https://live.trading212.com/")