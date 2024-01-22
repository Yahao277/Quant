# %% load files
import pandas as pd
import sys

sys.path.append('lib')
from lib.services.dr_info_pipeline import DrInfoPipeline
from lib.services.analyzer import Analyzer

# Load sample data with ts_event as datetime index
df = pd.read_csv('data/out/ES.ohlcv-1m.sample.csv', index_col='ts_event', parse_dates=True)

regular_df: pd.DataFrame = df.resample('5T').agg({'open': 'first',
                                                  'high': 'max',
                                                  'low': 'min',
                                                  'close': 'last',
                                                  'volume': 'sum'})
# drop nan values
regular_df.dropna(inplace=True)

#  Using Processor
analyzer = Analyzer()
pipeline = DrInfoPipeline(data=regular_df, analyzer=analyzer)

result = pipeline.run_pipeline()

result

