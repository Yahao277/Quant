import pandas as pd

from lib.services.session_service import SessionService


class DaySessionSplitter:
    def __init__(self):
        pass

    def process(self, data: pd.DataFrame):
        result = SessionService.split_by_day_session(data)
        return result
