# %% load files
import pandas as pd
import sys

sys.path.append('lib')

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
from lib.services.processor import Processor
from lib.services.analyzer import Analyzer
analyzer = Analyzer()
processor = Processor(data=regular_df, analyzer=analyzer)

# Draft cells
# %% processor sessions_group
processor.sessions_group

# %% DrInfo enrich draft
sessions_group = processor.sessions_group
