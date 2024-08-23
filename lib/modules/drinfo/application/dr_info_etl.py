
'''
UseCase: Transform ohlcv data info DrInfo data
ETL pipeline for DRInfo data
Here we will process OHLCV price data and prepare it for analysis

Input: OHLCV price data
Output: Processed DrInfo data stored into persistent storage

*DrInfo data: each day's session has 3 dr sessions: ADR, ODR, RDR.
'''
import pandas as pd

from lib.modules.drinfo.core.analyzer import Analyzer
from lib.modules.drinfo.core.processors.day_session_splitter import DaySessionSplitter
from lib.modules.drinfo.core.processors.dr_info_processor import DrInfoProcessor
from lib.modules.drinfo.core.processors.timezone_processor import TimezoneProcessor
from lib.modules.drinfo.dr_info_pipeline import DrInfoPipeline
from lib.modules.drinfo.persistence.price_csv_reader import PriceCsvReader
from lib.modules.drinfo.persistence.dataframe_writer import DataFrameWriter
from lib.modules.drinfo.persistence.dr_info_persistence import DrInfoPersistence
from lib.modules.drinfo.persistence.price_parquet_reader import PriceParquetReader


class DrInfoEtl:
    def __init__(self, data: pd.DataFrame, reader: PriceCsvReader, analyzer: Analyzer | None,
                 persistence: DrInfoPersistence, day_session_splitter: DaySessionSplitter,
                 timezone_processor: TimezoneProcessor, dr_info_processor: DrInfoProcessor):
        self.reader = reader
        self.analyzer = analyzer
        self.dr_info_persistence = persistence
        self.day_session_splitter = day_session_splitter
        self.timezone_processor = timezone_processor
        self.dr_info_processor = dr_info_processor
        self.data = data
        pass

    def run(self, df: pd.DataFrame):
        # 2. Process pipeline
        self.pipeline = DrInfoPipeline(data=df, analyzer=self.analyzer)
        result = self.pipeline.run_pipeline()
        # 3. Store processed data into persistent storage
        self.dr_info_persistence.store(result)
        pass

# %% Run main

reader = PriceParquetReader()
persistence = DrInfoPersistence()
day_session_splitter = DaySessionSplitter()
timezone_processor = TimezoneProcessor()
dr_info_processor = DrInfoProcessor()

# Read file
sample_file = 'data/out/nq/NQ.ohlcv-5m.202206-202208.sample.parquet'
data = reader.read(sample_file)




