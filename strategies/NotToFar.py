'''

STRATEGY ELABORATED MAINLY FOR TRADE ON FOREX AND FUTURES INSTRUMENTS.

DAY TRADING STARTEGY
5 MINUTES RANGE

INDICATORS:

Relative Strenght Index  - 7 Period
MACD
Bollinger Bands - 20 Period

'''


from __future__ import absolute_import, division, print_function, unicode_literals

import json

import backtrader as bt
from pync import Notifier


class strategy_nottofar(bt.Strategy):

    params = (
        ('rsi_period', 7),
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('BBandsperiod', 20)
    )

    def __init__(self):
        self.delayed = True
        self.name = self.data._name
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.params.macd1,
                                       period_me2=self.params.macd2,
                                       period_signal=self.params.macdsig)
        self.bband = bt.indicators.BBands(self.data, period=self.params.BBandsperiod)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.atr = bt.indicators.ATR(self.data, period=14)

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

