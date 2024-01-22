# %% load files
from datetime import timedelta
from typing import Optional

import pandas as pd
import sys

from pandas import Timestamp

from lib.models.session_dto import DrInfo, SessionDtoBuilder, SessionDto
from datetime import timedelta

from lib.services.enricher.dr_info_enricher import DrInfoEnricher
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

from lib.services.dr_info_pipeline import DrInfoPipeline
from lib.services.analyzer import Analyzer

analyzer = Analyzer()
processor = DrInfoPipeline(data=regular_df, analyzer=analyzer)

report = processor.analyze()

report

sessions_group = processor.sessions_group

# Get first session
session = sessions_group[sorted(sessions_group.keys())[0]]
first_day = sorted(sessions_group.keys())[0]


is_edt(first_day)
dr_sessions_times = SessionService.get_dr_sessions_times(first_day, is_edt(first_day))

# %%
dr_info_enricher = DrInfoEnricher()

session_dto = dr_info_enricher.enrich(session)

session_dto

