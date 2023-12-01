# %% load files
import pandas as pd
import sys

sys.path.append('lib')
from date_utils import is_edt
from services.session_service import SessionService


# Load sample data with ts_event as datetime index
df = pd.read_csv('data/out/ES.ohlcv-1m.sample.csv', index_col='ts_event', parse_dates=True)

regular_df: pd.DataFrame = df.resample('5T').agg({'open': 'first',
                                                  'high': 'max',
                                                  'low': 'min',
                                                  'close': 'last',
                                                  'volume': 'sum'})
# drop nan values
regular_df.dropna(inplace=True)

# %% Using Processor
from processor import Processor
from analyzer import Analyzer
analyzer = Analyzer()
processor = Processor(data=regular_df, analyzer=analyzer)

result = processor.process()

result

# Draft cells
# %% processor data
processor.sessions_group

# %% Split dataframes by sessions

# split data by session day
day_data = processor.sessions_group
count = 0
for day, session in day_data.items():
    count += 1
count
# %%

# regular_df groupby day
grouped = regular_df.groupby(regular_df.index.date)
# %%

for date, group in grouped:
    print(group)
    break


# Ideas
# create session_df - ok

# Split dataframe into dataframe by day session - ok

# Mark ADR, ORD, RDR session open and close time TODO

# Mark today's session open and close time - ok
