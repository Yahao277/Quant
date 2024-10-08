import datetime

from pandas._libs.tslibs.timestamps import Timestamp

from lib.models.session_dto import SessionDto, DrInfoBuilder, PricePoint, DrInfo
import pandas as pd

from lib.modules.drinfo.core.session_service import SessionService
from lib.utils.date_utils import is_edt


class DrInfoEnricher:
    def enrich(self, session_dto: SessionDto):
        dr_sessions_times = SessionService.get_dr_sessions_times(session_dto.close_time, is_edt(session_dto.close_time))
        adr_info, odr_info, rdr_info = self._apply_dr_info(session_dto.price_df, dr_sessions_times)
        session_dto.adr_info = adr_info
        session_dto.odr_info = odr_info
        session_dto.rdr_info = rdr_info
        return session_dto

    def enrich_group(self, sessions_group: dict[datetime, SessionDto]) -> dict[datetime, SessionDto]:
        enriched_sessions_group = {}
        for timekey in sessions_group:
            enriched_sessions_group[timekey] = self.enrich(sessions_group[timekey])
        return enriched_sessions_group

    def _apply_dr_info(self, session_df: pd.DataFrame, dr_sessions_times: dict[str, datetime]):
        adr_info: DrInfo = self.get_dr_info(session_df, dr_sessions_times, 'ADR')
        odr_info: DrInfo = self.get_dr_info(session_df, dr_sessions_times, 'ODR')
        rdr_info: DrInfo = self.get_dr_info(session_df, dr_sessions_times, 'RDR')
        return adr_info, odr_info, rdr_info

    def _dr_range_info(self, collector: DrInfoBuilder, session_df: pd.DataFrame, session_schedule: tuple,
                       session_type: str):
        collector.dr_type = session_type
        collector.dr_open = PricePoint(price=session_df.loc[session_schedule[0]], time=session_schedule[0])
        dr_close_time = session_schedule[0] + datetime.timedelta(hours=1)
        collector.dr_close = PricePoint(price=session_df.loc[dr_close_time], time=dr_close_time)

        dr_df = session_df[(session_df.index >= collector.dr_open.time) & (session_df.index < dr_close_time)]

        # DR High
        dr_high_time = dr_df['high'].idxmax()
        collector.dr_high = PricePoint(price=dr_df.loc[dr_high_time]['high'], time=dr_high_time)

        # DR Low
        dr_low_time = dr_df['low'].idxmin()
        collector.dr_low = PricePoint(price=dr_df.loc[dr_low_time]['low'], time=dr_low_time)

        # IDR High
        idr_high_time = dr_df[['open', 'close']].max(axis=1).idxmax()
        # dr_df.loc[idr_high_time][['open', 'close']].max(axis=1) TODO: test if works
        idr_high = dr_df[['open', 'close']].max(axis=1).max()
        collector.idr_high = PricePoint(price=idr_high, time=idr_high_time)

        # IDR Low
        idr_low_time = dr_df[['open', 'close']].min(axis=1).idxmin()
        # dr_df.loc[idr_low_time][['open', 'close']].min(axis=1) TODO: test if works
        idr_low = dr_df[['open', 'close']].min(axis=1).min()
        collector.idr_low = PricePoint(price=idr_low, time=idr_low_time)

        # Range
        collector.mid_idr_price = collector.idr_high.price + collector.idr_low.price / 2
        collector.dr_range = collector.dr_high.price - collector.dr_low.price
        collector.idr_range = collector.idr_high.price - collector.idr_low.price
        return collector, dr_df

    def _session_info(self, collector: DrInfoBuilder, session_df: pd.DataFrame, session_schedule: tuple):
        dr_session_df = session_df[
            (session_df.index >= session_schedule[0]) & (session_df.index < session_schedule[1])]

        collector.session_open = PricePoint(price=dr_session_df.iloc[0]['open'], time=dr_session_df.index[0])
        collector.session_close = PricePoint(price=dr_session_df.iloc[-1]['close'], time=dr_session_df.index[-1])

        dr_session_high_time = dr_session_df['high'].idxmax()
        # dr_session_high = dr_session_df['high'].max()
        collector.session_high = PricePoint(price=dr_session_df.loc[dr_session_high_time]['high'],
                                            time=dr_session_high_time)

        dr_session_low_time = dr_session_df['low'].idxmin()
        # dr_session_low = dr_session_df['low'].min()
        collector.session_low = PricePoint(price=dr_session_df.loc[dr_session_low_time]['low'],
                                           time=dr_session_low_time)
        return collector, dr_session_df

    def _confirmation_info(self, collector: DrInfoBuilder, dr_session_df: pd.DataFrame):
        touch_high = dr_session_df['high'] > collector.dr_high.price
        first_high_idx: Timestamp = touch_high.idxmax() if touch_high.any() else None
        touch_low = dr_session_df['low'] < collector.dr_low.price
        first_low_idx: Timestamp = touch_low.idxmax() if touch_low.any() else None

        # confirmation_day first_high_idx XOR first_low_idx condition
        collector.confirmation_type = bool(first_high_idx is not None) ^ bool(first_low_idx is not None)
        collector.has_confirmation = first_high_idx is not None or first_low_idx is not None

        collector.confirmation_direction = None
        collector.confirmation_time = None

        if collector.has_confirmation:
            candle_idx = first_high_idx if first_high_idx is not None else first_low_idx
            collector.confirmation_direction = 'Long' if first_high_idx is not None else 'Short'
            if collector.confirmation_type is False:
                if first_low_idx > first_high_idx:
                    candle_idx = first_high_idx
                    collector.confirmation_direction = 'Long'
                elif first_low_idx == first_high_idx:
                    candle_idx = first_high_idx
                    collector.confirmation_direction = 'Range'
                else:
                    candle_idx = first_low_idx
                    collector.confirmation_direction = 'Short'
            collector.confirmation_time = candle_idx
        return collector

    # column: 'high' | 'low'
    def __get_max_before(self, df: pd.DataFrame, ref_time, column) -> PricePoint | None:
        filtered_df = df[(df.index < ref_time)]
        if filtered_df.empty:
            return None
        max_time = filtered_df[column].idxmax() if column == 'high' else filtered_df[column].idxmin()
        max_value = filtered_df.loc[max_time, column]
        return PricePoint(price=max_value, time=max_time)

    def __calculate_std_values(self, price_point: PricePoint | None, ref_price: float, std_range: float):
        if price_point is None:
            return None
        return (price_point.price - ref_price) / std_range

    def __set_extension_info_by_direction(self, collector: DrInfoBuilder, session_df: pd.DataFrame,
                                          max_up: PricePoint, max_down: PricePoint, std_range: float,
                                          max_up_before_down: PricePoint | None, max_down_before_up: PricePoint | None):
        if collector.confirmation_direction == 'Long':
            collector.max_extension = max_up
            collector.max_retracement = max_down
            collector.max_extension_before_retracement = max_up_before_down
            collector.max_retracement_before_extension = max_down_before_up
            std_init_price, std_close_price = collector.idr_low.price, collector.idr_high.price
        else:
            collector.max_extension = max_down
            collector.max_retracement = max_up
            collector.max_extension_before_retracement = max_down_before_up
            collector.max_retracement_before_extension = max_up_before_down
            std_init_price, std_close_price = collector.idr_high.price, collector.idr_low.price

        collector.max_extension_std = self.__calculate_std_values(collector.max_extension, std_init_price, std_range)
        collector.max_retracement_std = self.__calculate_std_values(collector.max_retracement, std_init_price,
                                                                    std_range)
        collector.max_extension_before_retracement_std = self.__calculate_std_values(
            collector.max_extension_before_retracement, std_init_price, std_range)
        collector.max_retracement_before_extension_std = self.__calculate_std_values(
            collector.max_retracement_before_extension, std_init_price, std_range)
        return collector

    def _extension_retracement_info(self, collector: DrInfoBuilder, session_df: pd.DataFrame):
        std_range = collector.idr_high.price - collector.idr_low.price
        # from DR close to Session close (session price withou first hour)
        session_without_dr_df = session_df[
            (session_df.index > collector.dr_close.time) & (session_df.index < collector.session_close.time)]

        # max extension
        max_up_time = session_without_dr_df['high'].idxmax()
        max_up = session_without_dr_df.loc[max_up_time]['high']
        # max retracement
        max_down_time = session_without_dr_df['low'].idxmin()
        max_down = session_without_dr_df.loc[max_down_time]['low']

        # Calculate max extension/retracement before the opposite movement
        max_up_before_down = self.__get_max_before(session_without_dr_df, max_down_time, 'high')
        max_down_before_up = self.__get_max_before(session_without_dr_df, max_up_time, 'low')

        collector = self.__set_extension_info_by_direction(collector=collector,
                                                           session_df=session_without_dr_df,
                                                           max_up=PricePoint(price=max_up, time=max_up_time),
                                                           max_down=PricePoint(price=max_down, time=max_down_time),
                                                           max_up_before_down=max_up_before_down,
                                                           max_down_before_up=max_down_before_up,
                                                           std_range=std_range)
        return collector

    # session_type: 'ADR' | 'ODR' | 'RDR'
    def get_dr_info(self, session_df: pd.DataFrame, dr_sessions_times: dict[str, datetime], session_type: str):
        info_collect: DrInfoBuilder = DrInfoBuilder()
        session_schedule: tuple = dr_sessions_times[session_type]

        # DR range info (Only first hour of the session)
        # Collects: dr_high, dr_low, idr_high, idr_low, mid_idr, dr_range, idr_range
        info_collect, dr_df = self._dr_range_info(info_collect, session_df, session_schedule, session_type)

        # Entire session info
        # Collects: session_open, session_close, session_high, session_low
        info_collect, dr_session_df = self._session_info(info_collect, session_df, session_schedule)

        # Confirmation Info
        info_collect = self._confirmation_info(info_collect, dr_session_df)

        # Extension and Retracement Info
        info_collect = self._extension_retracement_info(info_collect, session_df)

        return info_collect.build()
