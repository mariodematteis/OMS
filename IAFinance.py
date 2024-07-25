from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.contract import Contract
from ibapi.order import *

import threading
import datetime
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []

    def historicalData(self, reqId, bar):
        epoch = datetime.datetime.fromtimestamp(int(bar.date)).strftime('%H:%M:%S %d/%m/%Y')
        print(f'Time: {epoch} Close: {bar.close}')
        self.data.append([bar.date, bar.close])

def run_loop():
    app.run()

def FX_contract(symbol):
	contract = Contract()
	contract.symbol = symbol[:3]
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = symbol[3:]
	return contract


app = IBapi()
app.connect('127.0.0.1', 7497, 123)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

