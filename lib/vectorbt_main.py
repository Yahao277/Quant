# %%
import time
from datetime import datetime, timedelta

import vectorbt as vbt
import pandas as pd
from numba import jit
import numpy as np

# Load sample data with ts_event as datetime index
#filepath = 'data/in/ES.ohlcv-1m.csv'
filepath = 'data/out/ES.ohlcv-1m.sample.csv'
df = pd.read_csv(filepath, index_col='ts_event', parse_dates=True)

# df: pd.DataFrame = df.resample('5T').agg({'open': 'first',
#                                                   'high': 'max',
#                                                   'low': 'min',
#                                                   'close': 'last',
#                                                   'volume': 'sum'})
# drop nan values
df.dropna(inplace=True)

print('data Loaded')

def run_backtest(data: np.ndarray):
    sma = vbt.MA.run(data, 50)
    sma_slow = vbt.MA.run(data, 200)
    entries = sma.ma_crossed_above(sma_slow)
    exits = sma.ma_crossed_below(sma_slow)
    pf = vbt.Portfolio.from_signals(data, entries, exits, fees=0.001)
    return pf.total_profit()


# %%

start = time.time()

run_backtest(df['close'].to_numpy())

end = time.time()
elapsed_time = end - start
print('Execution time:', elapsed_time, 'seconds')

# %%
# pandas Series get how many true values has
# entries[entries].index

start = time.time()

run_backtest(df['high'].to_numpy())

end = time.time()
elapsed_time = end - start
print('Execution time second:', elapsed_time, 'seconds')

# %% give entries when is true

# %%
size = pd.Series([1, -1, 1, -1])  # per row
price = pd.DataFrame(
    {'a': [1, 2, 3, 4],
     'b': [4, 3, 2, 1]})  # per element
direction = ['both', 'both']  # per column
fees = 0.01  # per frame

pf = vbt.Portfolio.from_orders(price, size, direction=direction, fees=fees)
orders = pf.orders
orders.buy.count()
pf.total_profit()

