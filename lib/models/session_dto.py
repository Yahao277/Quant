from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum
import pandas as pd
from dataclass_builder import dataclass_builder


class SessionType(Enum):
    ADR = 'ADR'
    ODR = 'ODR'
    RDR = 'RDR'


@dataclass
class PricePoint:
    price: float
    time: datetime


@dataclass
class DrInfo:
    # DR range info
    dr_type: str  # ADR, ORD, RDR
    dr_open: PricePoint
    dr_close: PricePoint
    dr_high: PricePoint
    dr_low: PricePoint
    idr_high: PricePoint
    idr_low: PricePoint
    dr_range: float
    idr_range: float
    mid_idr_price: float
    # Dr Session range info
    session_open: PricePoint
    session_close: PricePoint
    session_high: PricePoint
    session_low: PricePoint
    # Confirmation info
    confirmation_type: bool  # True: only one direction or False: both directions
    has_confirmation: bool
    confirmation_direction: str  # Long or Short or Range
    confirmation_time: datetime
    #confirmation_candle_type: str  # Wick or Body Candle
    # Extension Info
    max_extension: PricePoint
    max_retracement: PricePoint
    max_extension_before_retracement: Optional[PricePoint]
    max_retracement_before_extension: Optional[PricePoint]
    max_extension_std: float
    max_retracement_std: float
    max_extension_before_retracement_std: float
    max_retracement_before_extension_std: float


DrInfoBuilder = dataclass_builder(DrInfo)


@dataclass
class SessionDto:
    close_time: datetime
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    price_df: pd.DataFrame
    adr_info: Optional[DrInfo] = None
    odr_info: Optional[DrInfo] = None
    rdr_info: Optional[DrInfo] = None

def to_dataframe(data: SessionDto) -> pd.DataFrame:

    pass

SessionDtoBuilder = dataclass_builder(SessionDto)
