import pandas as pd

from lib.analyzer import Analyzer
from lib.date_utils import is_edt
from lib.services.session_service import SessionService

'''
process, clean, transform futures price data to be ready for analysis and iteration
'''


class Processor:
    '''
    data: pd.DataFrame -> resampled 5minutes data
    '''

    def __init__(self, data: pd.DataFrame, analyzer: Analyzer | None):
        self.result = None
        self.data = data
        self.analyzer = analyzer
        self._preprocess()

    # define a preprocess private method
    def _preprocess(self):
        self.data['timestamp'] = self.data.index.map(lambda x: x.to_pydatetime().replace(tzinfo=None))
        self.data['timezone'] = self.data.index.map(
            lambda x: 'EDT' if is_edt(x.to_pydatetime().replace(tzinfo=None)) else 'EST')
        self.sessions_group = SessionService.split_by_day_session(self.data)
        self.sorted_sessions = sorted(self.sessions_group.keys())

    def process(self):
        self.analyzer.reset()
        for key in self.sorted_sessions:
            session_data = self.sessions_group[key]
            self.analyzer.analyze(session_data, self.data)
        self.result = self.analyzer.report()
        return self.result
