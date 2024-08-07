# %%
import backtrader as bt
from datetime import datetime
import pandas as pd
from lib.strategies.sma_cross import SmaCross

df = pd.read_csv('data/out/ES.ohlcv-1m.sample.csv', index_col='ts_event', parse_dates=True)

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# %% Create a data feed
# Load Data
data = bt.feeds.PandasData(dataname=df, fromdate=datetime(2017, 5, 21), todate=datetime(2017, 6, 1))

cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=30)

# cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy

# %% Run Backtest
print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.run()  # run it all
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
# %% Plot
cerebro.plot()