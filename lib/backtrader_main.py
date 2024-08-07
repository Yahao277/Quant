# %%
import time

import backtrader as bt
from datetime import datetime
import pandas as pd
from lib.strategies.sma_cross import SmaCross

filepath = '../data/in/ES.ohlcv-1m.csv'
#filepath = '../data/in/ES.ohlcv-1m.sample.csv'
df = pd.read_csv(filepath, index_col='ts_event', parse_dates=True)

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# %% Create a data feed
# Load Data
data = bt.feeds.PandasData(dataname=df)

cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=1)

# cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy

# %% Run Backtest
start = time.time()
#print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.run()  # run it all
end = time.time()
#print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
elapsed_time = end - start
print('Execution time:', elapsed_time, 'seconds')
# %% Plot

# cerebro.plot()