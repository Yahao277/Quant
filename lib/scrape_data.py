import databento as db
import pandas as pd
import numpy as np
# %%
client = db.Historical('db-4kXRPcWr9yDsi8uY75JGykRGcDbaB')
data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    stype_in='continuous',
    symbols=["ES.v.0"],
    schema="ohlcv-1m",
    start="2017-05-21T00:00",
    end="2023-11-12T023:50"
)


# %%
data.to_df().head()
# %%
csv_path = 'data/in/ES.ohlcv-1m.csv'
data.to_csv(csv_path)