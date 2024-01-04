from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas as pd


@dataclass
class PricePointInfo:
    price: float
    time: datetime


@dataclass
class DrInfo:
    # DR range info
    dr_type: str  # ADR, ORD, RDR
    dr_close: datetime
    dr_range: float
    idr_range: float
    dr_high: PricePointInfo
    dr_low: PricePointInfo
    idr_high: PricePointInfo
    idr_low: PricePointInfo
    mid_idr_price: float
    # Dr Session range info
    session_open: PricePointInfo
    session_close: PricePointInfo
    session_high: PricePointInfo
    session_low: PricePointInfo
    # Confirmation info
    confirmation_day: bool  # True: only one direction or False: both directions
    confirmation_direction: str  # Long or Short
    confirmation_time: datetime
    confirmation_candle_type: str  # Wick or Body Candle


@dataclass
class SessionDto:
    close_time: datetime
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    price_df: pd.DataFrame
    dr_info: Optional[DrInfo] = None
