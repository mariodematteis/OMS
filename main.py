from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from strategies.NotToFar import strategy_nottofar
import threading

threads_ = []
new_request = False

stockkwargs = dict(
    timeframe=bt.TimeFrame.Ticks,
    what='BID',
    historical=False,
    qcheck=0.5,
    latethrough=False,
    tradename=None,
    tz="Europe/Rome"
)


def handleInstruments(name, timerange, compression, strategies):
    global cerebro
    global ibstore
    data = ibstore.getdata(dataname=name, **stockkwargs)
    if timerange.lower() == "ticks":
        cerebro.resampledata(data, timeframe=1, compression=int(compression))
    elif timerange.lower() == "microseconds":
        cerebro.resampledata(data, timeframe=2, compression=int(compression))
    elif timerange.lower() == "seconds":
        cerebro.resampledata(data, timeframe=3, compression=int(compression))
    elif timerange.lower() == "minutes":
        cerebro.resampledata(data, timeframe=4, compression=int(compression))
    elif timerange.lower() == "days":
        cerebro.resampledata(data, timeframe=5, compression=int(compression))
    elif timerange.lower() == "months":
        cerebro.resampledata(data, timeframe=6, compression=int(compression))
    elif timerange.lower() == "weeks":
        cerebro.resampledata(data, timeframe=7, compression=int(compression))
    elif timerange.lower() == "months":
        cerebro.resampledata(data, timeframe=8, compression=int(compression))
    elif timerange.lower() == "years":
        cerebro.resampledata(data, timeframe=9, compression=int(compression))

    for strategy in strategies:
        print("ADDING " + strategy + "...")
        if strategy.lower() == "nottofar":
            cerebro.addstrategy(strategy_nottofar)
            print("NotToFar strategy added.")
            global new_request
            new_request = False
        else:
            print("UNKNOWN STRATEGY.")
            prompt()
    cerebro.run()


def prompt():
    command = input("> ")
    if command.upper() == "NEW ALGORITHM" or command == "1":
        json_strategies = []
        type_instrument = input("TYPE OF INSTRUMENT: ")
        name_instrument = input("NAME OF INSTRUMENT (NUM.DEN): ")
        time_range = input("TIME RANGE: ")
        compression = input("COMPRESSION: ")
        strategies_ = input("SINGLE ONE? ")
        if strategies_.lower() == "no" or strategies_.lower() == "n":
            list_of_strategies = input("WRITE STRATEGIES SEPARATED BY A COMMA: ")
            json_strategies = list_of_strategies.split(",")
        elif strategies_.lower() == "yes" or strategies_.lower() == "y":
            list_of_strategies = input("WHICH ONE? ")
            json_strategies.append(list_of_strategies)
        else:
            print("UNKNOWN COMMAND")
            prompt()

        if type_instrument.lower() == "fx" or type_instrument.lower() == "forex":
            name_ = name_instrument + "-CASH-IDEALPRO"
            thread = threading.Thread(target=handleInstruments, args=(name_, time_range, compression, json_strategies), daemon=False)
            threads_.append(thread)
            thread.start()
            if new_request:
                prompt()
        else:
            print("UNKNOWN COMMAND OR NOT STILL AVAILABLE")
            prompt()
    else:
        print("UNKNOWN COMMAND")
        prompt()


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    ibstore = bt.stores.IBStore(host="127.0.0.1", port=7497)
    prompt()
