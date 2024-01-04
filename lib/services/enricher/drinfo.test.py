# %% load files
from datetime import timedelta

import pandas as pd
import sys

from lib.models.session_dto import DrInfo
from datetime import timedelta
from lib.services.session_service import SessionService
from lib.utils.date_utils import *

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

report = processor.analyze()

report

# %%
sessions_group = processor.sessions_group

# Get first session
session = sessions_group[sorted(sessions_group.keys())[0]]
first_day = sorted(sessions_group.keys())[0]
# %% DrInfoEnricher enrich method draft

is_edt(first_day)
dr_sessions_times = SessionService.get_dr_sessions_times(first_day, is_edt(first_day))
# %% Dr Range (dr session's first hour)
session_df = session.price_df
adr_session = dr_sessions_times['ADR']
# adr_info = DrInfo()
drsession_open = adr_session[0]
drsession_close = adr_session[1]

# dr_range = close + timedelta 1 hour
dr_open = drsession_open
dr_close = drsession_open + timedelta(hours=1)

# Get dataframe between dr_open and dr_close
dr_df = session_df[(session_df.index >= dr_open) & (session_df.index < dr_close)]

# DR/IDR info
dr_high = dr_df['high'].max()
dr_high_time = dr_df['high'].idxmax()

dr_low = dr_df['low'].min()
dr_low_time = dr_df['low'].idxmin()
# idr high is the highest open or close price in dr_df
idr_high_series = dr_df[['open', 'close']].max(axis=1)
idr_high_time = idr_high_series.idxmax()
idr_high = idr_high_series.max()

idr_low_series = dr_df[['open', 'close']].min(axis=1)
idr_low_time = idr_low_series.idxmin()
idr_low = idr_low_series.min()

mid_idr = (idr_high + idr_low) / 2

idr_low, idr_low_time, mid_idr

# %%
# Dr Session range info (entire session)
drsession_df = session_df[(session_df.index >= drsession_open) & (session_df.index < drsession_close)]

drsession_open = drsession_df.iloc[0]['open']
drsession_close = drsession_df.iloc[-1]['close']
drsession_high = drsession_df['high'].max()
drsession_high_time = drsession_df['high'].idxmax()
drsession_low = drsession_df['low'].min()
drsession_low_time = drsession_df['low'].idxmin()

drsession_open, drsession_close, drsession_high, drsession_low, drsession_high_time, drsession_low_time


# %%
# Confirmation info
# drsession_df iterate and find confirmation candle (confirmation is the candle that has higher or lower then dr_low or dr_high)
# confirmation_candle_type = 'Wick' if confirmation_candle['high'] or confirmation_candle['low'] is dr_high or dr_low else 'Body'
# confirmation_direction = 'Long' if confirmation_candle['high'] is dr_high else 'Short'
# confirmation_time = confirmation_candle['time']
# confirmation_day = True if confirmation_candle['time'] is between dr_open and dr_close else False
def confirmation_info(time ,row: pd.Series, confirmation_dir: str | None, dir: str):
    return row, dir, time


confirmation_candle = None
confirmation_direction = None
confirmation_time = None
confirmation_day = None
time_touches_high = None
time_touches_low = None
for index, row in drsession_df.iterrows():
    if row['high'] >= dr_high and time_touches_high is None:
        time_touches_high = index
        if confirmation_candle is None:
            confirmation_candle, confirmation_direction, confirmation_time = confirmation_info(index, row, confirmation_direction, 'Long')
            break
    if row['low'] <= dr_low and time_touches_low is None:
        time_touches_low = index
        if confirmation_candle is None:
            confirmation_candle, confirmation_direction, confirmation_time = confirmation_info(index, row, confirmation_direction, 'Short')
            break
    # Break the loop if both conditions are met
    if time_touches_high is not None and time_touches_low is not None:
        break
confirmation_day = not (time_touches_high and time_touches_low)

# odr_info = DrInfo()
#
# rdr_info = DrInfo()
# Enrich DRInfo

# %%
# TODO: add Extension, Retracement, Reversal info

# %%
