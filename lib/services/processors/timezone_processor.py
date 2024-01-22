import pandas as pd

from lib.utils.date_utils import is_edt


class TimezoneProcessor:
    def __init__(self):
        pass
    # Input:
    # data = pd.DataFrame with datetime as index
    # Returns:
    # data = pd.DataFrame adding timezone column
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['timestamp'] = data.index.map(lambda x: x.to_pydatetime().replace(tzinfo=None))
        data['timezone'] = data.index.map(
            lambda x: 'EDT' if is_edt(x.to_pydatetime().replace(tzinfo=None)) else 'EST')
        return data
