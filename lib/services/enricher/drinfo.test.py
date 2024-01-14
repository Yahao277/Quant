# %% load files
from datetime import timedelta
from typing import Optional

import pandas as pd
import sys

from pandas import Timestamp

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
dr_session_df = session_df[(session_df.index >= drsession_open) & (session_df.index < drsession_close)]

drsession_open = dr_session_df.iloc[0]['open']
drsession_close = dr_session_df.iloc[-1]['close']
drsession_high = dr_session_df['high'].max()
drsession_high_time = dr_session_df['high'].idxmax()
drsession_low = dr_session_df['low'].min()
drsession_low_time = dr_session_df['low'].idxmin()

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

# odr_info = DrInfo()
#
# rdr_info = DrInfo()
# Enrich DRInfo
# %%
touch_high = dr_session_df['high'] > dr_high
first_high_idx: Timestamp = touch_high.idxmax() if touch_high.any() else None
touch_low = dr_session_df['low'] < dr_low
first_low_idx: Timestamp = touch_low.idxmax() if touch_low.any() else None

# %%
# confirmation_day first_high_idx XOR first_low_idx condition
confirmation_type = bool(first_high_idx is not None) ^ bool(first_low_idx is not None)
has_confirmation = first_high_idx is not None or first_low_idx is not None

confirmation_direction, confirmation_time, confirmation_candle = None, None, None

if has_confirmation:
    candle_idx = first_high_idx if first_high_idx is not None else first_low_idx
    confirmation_direction = 'Long' if first_high_idx is not None else 'Short'
    if confirmation_type is False:
        if first_low_idx > first_high_idx:
            candle_idx = first_high_idx
            confirmation_direction = 'Long'
        elif first_low_idx == first_high_idx:
            candle_idx = first_high_idx
            confirmation_direction = 'None'
        else:
            candle_idx = first_low_idx
            confirmation_direction = 'Short'
    confirmation_candle = dr_session_df.loc[candle_idx]
    confirmation_time = candle_idx



# %%
#   Extension, Retracement
# - Standard deviation 0.1 lines grid
#
# returns
# - max extension (maxE)
# - max retracement (maxR)
# - max extension before max retracement (maxE2R)
# - max retracement before max extension (maxR2E)
std_range = idr_high - idr_low
# dr_session_df from dr_close to drsession_close
session_without_dr_df = session_df[(session_df.index > dr_close) & (session_df.index < drsession_close)]

# max extension
max_up = session_without_dr_df['high'].max()
max_up_time = session_without_dr_df['high'].idxmax()
# max retracement
max_down = session_without_dr_df['low'].min()
max_down_time = session_without_dr_df['low'].idxmin()

# max extension before max retracement
max_up_before_down = session_without_dr_df[(session_without_dr_df.index < max_down_time)].max()
max_up_before_down_time = max_up_before_down.idxmax()

# max retracement before max extension
max_down_before_up = session_without_dr_df[(session_without_dr_df.index < max_up_time)]
max_down_before_up_time = max_down_before_up.idxmin()

if confirmation_direction == 'Long':
    max_extension = max_up
    max_extension_time = max_up_time
    max_retracement = max_down
    max_retracement_time = max_down_time
    max_extension_before_retracement = max_up_before_down
    max_extension_before_retracement_time = max_up_before_down_time
    max_retracement_before_extension = max_down_before_up
    max_retracement_before_extension_time = max_down_before_up_time
else:
    max_extension = max_down
    max_extension_time = max_down_time
    max_retracement = max_up
    max_retracement_time = max_up_time
    max_extension_before_retracement = max_down_before_up
    max_extension_before_retracement_time = max_down_before_up_time
    max_retracement_before_extension = max_up_before_down
    max_retracement_before_extension_time = max_up_before_down_time

std_range = idr_high - idr_low
# express max extension and max retracement as percentage of std_range
max_extension_percent = (max_extension - idr_low) / std_range
max_retracement_percent = (idr_high - max_retracement) / std_range
max_extension_before_retracement_percent = (max_extension_before_retracement - idr_low) / std_range
max_retracement_before_extension_percent = (idr_high - max_retracement_before_extension) / std_range
# %%
