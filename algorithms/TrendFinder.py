from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt

from decimal import Decimal
import datetime
from numpy import log
import json
import threading

import numpy as np

stockkwargs = dict(
    timeframe=bt.TimeFrame.Ticks,
    what='BID',
    fromdate=datetime.datetime(year=2021, month=3, day=4),
    todate=datetime.datetime(year=2021, month=6, day=4),
    historical=True,
    qcheck=0.5,
    latethrough=False,
    tradename=None,
    tz="Europe/Rome"
)

dates = []
closeprices = []
openprices = []
highprices = []
lowprices = []
bbtop = []
bbbottom = []
bbmid = []
rsiArray = []
stochasticArray = []
adxArray = []
cciArray = []
dmiArray = []
momentumArray = []
macdArray = []
signalArray = []
stddevArray = []
sma7Array = []
sma10Array = []
sma20Array = []
sma50Array = []
sma100Array = []

downloaded = False
triggered = False

def trigger(cerebro_):
    while True:
        if triggered:
            cerebro_.runstop()
            print("Data downloaded")
            break

class Downloader(bt.Strategy):

    def __init__(self):
        self.name = self.data._name
        self.dates_ = []
        self.rsi = bt.indicators.RSI(self.data, period=7)
        self.stochastic_slow = bt.indicators.Stochastic(self.data, upperband=75.0, lowerband=25.0, safediv=True)
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.data)
        self.cci = bt.indicators.CommodityChannelIndex(self.data)
        self.dmi = bt.indicators.DirectionalMovementIndex(self.data)
        self.momentumK = bt.indicators.Momentum(self.stochastic_slow.percK, period=18)
        self.bb__top = bt.indicators.BollingerBands(self.data)
        self.bb__bottom = bt.indicators.BollingerBands(self.data)
        self.bb__mid = bt.indicators.BollingerBands(self.data)
        self.macd = bt.indicators.MACD(self.data)
        self.stddev = bt.indicators.StandardDeviation(self.data, period=7)
        self.sma7_arr = bt.indicators.SmoothedMovingAverage(self.data, period=7)
        self.sma10_arr = bt.indicators.SmoothedMovingAverage(self.data, period=10)
        self.sma20_arr = bt.indicators.SmoothedMovingAverage(self.data, period=20)
        self.sma50_arr = bt.indicators.SmoothedMovingAverage(self.data, period=50)
        self.sma100_arr = bt.indicators.SmoothedMovingAverage(self.data, period=100)
        self.stochastic = []
        self.rsi_ = []
        self.adx_ = []
        self.cci_ = []
        self.dmi_ = []
        self.momentumK_array = []
        self.close = []
        self.open = []
        self.high = []
        self.low = []
        self.bb_top = []
        self.bb_bottom = []
        self.bb_mid = []
        self.macd_ = []
        self.signal_ = []
        self.stddev_ = []
        self.sma7Array_ = []
        self.sma10Array_ = []
        self.sma20Array_ = []
        self.sma50Array_ = []
        self.sma100Array_ = []


    def notify_data(self, data, status, *args, **kwargs):
        if status == data.DISCONNECTED:
            global dates
            global closeprices
            global openprices
            global highprices
            global lowprices
            global bbtop
            global bbbottom
            global bbmid
            global rsiArray
            global stochasticArray
            global adxArray
            global cciArray
            global dmiArray
            global momentumArray
            global downloaded
            global macdArray
            global signalArray
            global stddevArray
            global sma7Array
            global sma10Array
            global sma20Array
            global sma50Array
            global sma100Array
            dates = self.dates_
            closeprices = self.close
            openprices = self.open
            highprices = self.high
            lowprices = self.low
            bbtop = self.bb_top
            bbbottom = self.bb_bottom
            bbmid = self.bb_mid
            rsiArray = self.rsi_
            stochasticArray = self.stochastic
            adxArray = self.adx_
            cciArray = self.cci_
            dmiArray = self.dmi_
            momentumArray = self.momentumK_array
            macdArray = self.macd_
            signalArray = self.signal_
            stddevArray = self.stddev_
            sma7Array = self.sma7Array_
            sma10Array = self.sma10Array_
            sma20Array = self.sma20Array_
            sma50Array = self.sma50Array_
            sma100Array = self.sma100Array_
            downloaded = True
        elif status == data.LIVE:
            if len(self.close) > 200:
                global triggered
                triggered = True


    def next(self):
        _candleInfo = {"DATETIME": self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"),
                       "OPEN": self.data.open[0]}
        print(json.dumps(_candleInfo))
        self.dates_.append(self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"))
        self.close.append(self.data.close[0])
        self.open.append(self.data.open[0])
        self.high.append(self.data.high[0])
        self.low.append(self.data.low[0])
        self.bb_top.append(self.bb__top.lines.top[0])
        self.bb_bottom.append(self.bb__bottom.lines.bot[0])
        self.bb_mid.append(self.bb__mid.lines.mid[0])
        self.rsi_.append(self.rsi[0])
        self.adx_.append(self.adx[0])
        self.cci_.append(self.cci[0])
        self.dmi_.append(self.dmi[0])
        self.stochastic.append(self.stochastic_slow[0])
        self.momentumK_array.append(self.momentumK[0])
        self.macd_.append(self.macd.macd[0])
        self.signal_.append(self.macd.signal[0])
        self.stddev_.append(self.stddev[0])
        self.sma7Array_.append(self.sma7_arr[0])
        self.sma10Array_.append(self.sma10_arr[0])
        self.sma20Array_.append(self.sma20_arr[0])
        self.sma50Array_.append(self.sma50_arr[0])
        self.sma100Array_.append(self.sma100_arr[0])

        dates.append(self.data.datetime.datetime(0).strftime("%d/%m/%Y, %H:%M:%S"))
        closeprices.append(self.data.close[0])
        openprices.append(self.data.open[0])
        highprices.append(self.data.high[0])
        lowprices.append(self.data.low[0])
        bbtop.append(self.bb__top.lines.top[0])
        bbbottom.append(self.bb__bottom.lines.bot[0])
        bbmid.append(self.bb__mid.lines.mid[0])
        rsiArray.append(self.rsi[0])
        stochasticArray.append(self.stochastic_slow[0])
        adxArray.append(self.adx[0])
        cciArray.append(self.cci[0])
        dmiArray.append(self.dmi[0])
        momentumArray.append(self.momentumK[0])
        macdArray.append(self.macd.macd[0])
        signalArray.append(self.macd.signal[0])
        stddevArray.append(self.stddev[0])
        sma7Array.append(self.sma7_arr[0])
        sma10Array.append(self.sma10_arr[0])
        sma20Array.append(self.sma20_arr[0])
        sma50Array.append(self.sma50_arr[0])
        sma100Array.append(self.sma100_arr[0])



def DownloadData():
    cerebro = bt.Cerebro()
    ibstore = bt.stores.IBStore(host="127.0.0.1", port=7497)
    thread = threading.Thread(target=trigger, args=(cerebro, ))
    thread.start()
    data = ibstore.getdata(dataname="GBP.USD-CASH-IDEALPRO", **stockkwargs)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)
    cerebro.addstrategy(Downloader)
    cerebro.run()

    return [dates, openprices, closeprices, highprices, lowprices, bbtop, bbmid, bbbottom, rsiArray, stochasticArray, adxArray, cciArray, dmiArray, momentumArray, macdArray, signalArray, stddevArray, sma7Array, sma10Array, sma20Array, sma50Array, sma100Array]


class TrendFinder:

    def __init__(self, data) -> None:
        super().__init__()
        self.array = data
        self.len_array = len(data)
        self.nameArray = self.arrayName()
        self.dateTimeArray = self.arrayDatetime()
        self.closePricesArray = self.arrayClosePrices()
        self.arrayTrends = {}
        self.listLN = []
        self.LNListGenerator(self.closePricesArray)
        self.response = {"MESSAGE": "NONE"}
        self.dataAvailability = False
        if self.len_array > 0:
            self.dataAvailability = True

        self.locateTrends()

    def arrayName(self):
        arrayName_ = []
        for counter in range(0, self.len_array):
            arrayName_.append(self.array[counter][0])
        return arrayName_

    def arrayDatetime(self):
        arrayDatetime_ = []
        for counter in range(0, self.len_array):
            arrayDatetime_.append(self.array[counter][1])
        return arrayDatetime_

    def arrayClosePrices(self):
        arrayPrices_ = []
        for counter in range(0, self.len_array):
            arrayPrices_.append(self.array[counter][2])
        return arrayPrices_

    def valueLN(self, number):
        return abs(log(float(number)))

    def LNListGenerator(self, data):
        for counter in range(0, self.len_array):
            difference = data[counter] - data[counter - 1]
            value = abs(Decimal(f'{difference:.5f}'))
            self.listLN.append(self.valueLN(value))

        return self.listLN

    def locateTrends(self):
        tempArray = []
        data = np.array(self.listLN)
        print(self.listLN)
        print(data.argmin())
        localCounter = 1
        while self.dataAvailability:
            print("ARRIVED HERE")
            while self.listLN[data.argmin()] < self.listLN[data.argmin() + localCounter]:
                tempArray.append([self.nameArray[data.argmin() + localCounter], self.dateTimeArray[data.argmin() + localCounter], self.closePricesArray[data.argmin() + localCounter]])
                self.nameArray.pop(data.argmin())
                self.dateTimeArray.pop(data.argmin())
                self.closePricesArray.pop(data.argmin())
                np.delete(data, data.argmin())
                localCounter += 1
                self.len_array -= 1
                #print(data.argmin())

                if localCounter == len(self.closePricesArray):
                    self.dataAvailability = False

                if self.len_array == 0:
                    self.dataAvailability = False


        print(tempArray)



