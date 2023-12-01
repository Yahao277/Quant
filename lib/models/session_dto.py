from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class SessionDto:
    close_time: datetime
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    price_df: pd.DataFrame
