import databento as db
import pandas as pd
import numpy as np
# %%
apikey = ''
client = db.Historical(apikey)
data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    stype_in='continuous',
    symbols=["NQ.v.0"],
    schema="ohlcv-1s",
    start="2021-09-01T00:00",
    end="2024-05-28T00:00"
)


# %%
data.to_df().head()
# %%
csv_path = 'data/in/NQ.ohlcv-1s.202109-202405-2.csv'
data.to_csv(csv_path)