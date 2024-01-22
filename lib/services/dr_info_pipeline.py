import pandas as pd

from lib.services.analyzer import Analyzer
from lib.services.enricher.dr_info_enricher import DrInfoEnricher
from lib.services.processors.day_session_splitter import DaySessionSplitter
from lib.services.processors.dr_info_processor import DrInfoProcessor
from lib.services.processors.timezone_processor import TimezoneProcessor
from lib.utils.date_utils import (is_edt)
from lib.services.session_service import SessionService

'''
process, clean, transform futures price data to be ready for analysis and iteration
'''


class DrInfoPipeline:
    '''
    data: pd.DataFrame -> resampled 5minutes data
    '''

    def __init__(self, data: pd.DataFrame, analyzer: Analyzer | None):
        self.report = None
        self.result = None
        self.data = data
        self.analyzer = analyzer
        self.day_session_splitter = DaySessionSplitter()
        self.dr_info_processor = DrInfoProcessor()
        self.timezone_processor = TimezoneProcessor()
        self.pipeline = [self.timezone_processor, self.day_session_splitter, self.dr_info_processor]

    # define a preprocess private method
    def run_pipeline(self):
        self.result = self.timezone_processor.process(self.data)
        self.result = self.day_session_splitter.process(self.result)
        self.result = self.dr_info_processor.process(self.result)
        return self.result

    '''
    Process each day's session and let analyzer to make custom analysis
    '''
    def analyze(self):
        self.analyzer.reset()
        for key in self.dr_info_processor.sorted_sessions:
            session_data = self.sessions_group[key]
            self.analyzer.analyze(session_data, self.data)
        self.report = self.analyzer.report()
        return self.report
