import datetime

from lib.models.session_dto import SessionDto
import pandas as pd

from lib.services.session_service import SessionService
from lib.utils.date_utils import is_edt


class DrInfoEnricher:
    def __init__(self, dr_info):
        self.dr_info = dr_info

    def enrich(self, session_dto: SessionDto):
        dr_sessions_times = SessionService.get_dr_sessions_times(session_dto.close_time, is_edt(session_dto.close_time))
        self._dr_range(session_dto.price_df, dr_sessions_times)
        return session_dto

    def enrich_group(self, sessions_group: dict[datetime, SessionDto]):
        enriched_sessions_group = {}
        for key in sessions_group:
            enriched_sessions_group[key] = self.enrich(sessions_group[key])
        return enriched_sessions_group

    def _dr_range(self, session_df: pd.DataFrame, dr_sessions_times: dict[str, datetime]):
        self._dr_session_info(session_df, dr_sessions_times, 'ADR')
        self._dr_session_info(session_df, dr_sessions_times, 'ODR')
        self._dr_session_info(session_df, dr_sessions_times, 'RDR')
        pass

    # session_type: 'ADR' | 'ODR' | 'RDR'
    def _dr_session_info(self, session_df: pd.DataFrame, dr_sessions_times: dict[str, datetime], session_type: str):
        dr_session = dr_sessions_times[session_type]
        dr_session_open_time = dr_session[0]
        dr_session_close_time = dr_session[1]
        dr_open_time = dr_session_open_time
        dr_close_time = dr_session_open_time + datetime.timedelta(hours=1)
        dr_df = session_df[(session_df.index >= dr_open_time) & (session_df.index < dr_close_time)]
        dr_high = dr_df['high'].max()
        dr_high_time = dr_df['high'].idxmax()
        dr_low = dr_df['low'].min()
        dr_low_time = dr_df['low'].idxmin()
        idr_high_series = dr_df[['open', 'close']].max(axis=1)
        idr_high_time = idr_high_series.idxmax()
        idr_high = idr_high_series.max()
        idr_low_series = dr_df[['open', 'close']].min(axis=1)
        idr_low_time = idr_low_series.idxmin()
        idr_low = idr_low_series.min()
        mid_idr = (idr_high + idr_low) / 2

        # Entire session info
        dr_session_df = session_df[(session_df.index >= dr_session_open_time) & (session_df.index < dr_session_close_time)]
        dr_session_open = dr_session_df.iloc[0]['open']
        dr_session_close = dr_session_df.iloc[-1]['close']
        dr_session_high = dr_session_df['high'].max()
        dr_session_high_time = dr_session_df['high'].idxmax()
        dr_session_low = dr_session_df['low'].min()
        dr_session_low_time = dr_session_df['low'].idxmin()

        # ConfirmationInfo TODO
        
        pass