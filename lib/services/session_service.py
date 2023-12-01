from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz

from date_utils import find_transition_dates

from lib.models.session_dto import SessionDto


class SessionService:
    # Function to get session boundaries in Eastern Time, read README.md for more details
    @staticmethod
    def get_session_boundaries(day: datetime) -> (datetime, datetime):
        est_to_edt, edt_to_est = find_transition_dates(day.year)
        if est_to_edt <= day < edt_to_est:  # EDT session
            session_start = datetime(day.year, day.month, day.day, 22, 0, 0, tzinfo=None) - timedelta(days=1)
            session_end = datetime(day.year, day.month, day.day, 21, 0, 0, tzinfo=None)
        else:  # EST session
            session_start = datetime(day.year, day.month, day.day, 23, 0, 0, tzinfo=None) - timedelta(days=1)
            session_end = datetime(day.year, day.month, day.day, 22, 0, 0, tzinfo=None)
        return session_start, session_end

    '''
    Dictionary of session times for each day
    key: datetime no timezone and time 00:00:00 (only date)
    value: 
        {
            'opentime': datetime with timezone,
            'closetime': datetime with timezone,
            'open': float,
            'high': float,
            'low': float,
            'close': float,
            'price_df': pd.DataFrame TODO: add price_df
        }
    '''
    @staticmethod
    def split_by_day_session(price_df: pd.DataFrame) -> dict[datetime, SessionDto]:
        # split data by session day
        day_data = {}
        for date, group in price_df.groupby(price_df.index.date):
            day = datetime.combine(date, datetime.min.time())
            start, end = SessionService.get_session_boundaries(day)
            start_utc = pytz.utc.localize(start)
            end_utc = pytz.utc.localize(end)
            session_data = price_df[(price_df.index >= start_utc) & (price_df.index <= end_utc)]
            if not session_data.empty:
                day_data[day] = SessionDto(
                    open_time=session_data.index[0],
                    close_time=session_data.index[-1],
                    open=session_data.iloc[0]['open'],
                    high=session_data['high'].max(),
                    low=session_data['low'].min(),
                    close=session_data.iloc[-1]['close'],
                    price_df=session_data
                )
        return day_data





