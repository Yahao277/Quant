'''
Use case: Resample NQ Price Data
ResamplingNqPrice class is used to resample the price data of nasdaq.
Our original ohlcv data downloaded from Databento is in 1 second interval.
We have to resample into the timeframe we want to analyze.
'''
import pandas as pd

from lib.modules.drinfo.persistence.dataframe_writer import DataFrameWriter
from lib.modules.drinfo.persistence.price_csv_reader import PriceCsvReader
from lib.modules.drinfo.persistence.price_parquet_reader import PriceParquetReader


class ResamplingNqPrice:
    def __init__(self, reader: PriceCsvReader | PriceParquetReader, df_writer: DataFrameWriter):
        self.reader = reader
        self.df_writer = df_writer
        self.df: pd.DataFrame = None

    def process_task(self, input_path, output_path, timeframe='5T'):
        if self.df is None:
            self.df = self.reader.read(file_path=input_path)

        # Resample ohlcv data
        regular_df: pd.DataFrame = self.df.resample(timeframe).agg({'open': 'first',
                                                               'high': 'max',
                                                               'low': 'min',
                                                               'close': 'last',
                                                               'volume': 'sum'})
        # drop nan values
        regular_df.dropna(inplace=True)

        self.df_writer.save(regular_df, output_path)
        return True

    def sample_data_task(self, input_path, output_path, timeframe='5T'):
        if self.df is None:
            self.df = self.reader.read(file_path=input_path)

        start_date = pd.to_datetime('2022-06').tz_localize('UTC')
        end_date = pd.to_datetime('2022-08').tz_localize('UTC')

        regular_df = self.df[start_date:end_date]

        # Resample ohlcv data
        regular_df: pd.DataFrame = regular_df.resample(timeframe).agg({'open': 'first',
                                                               'high': 'max',
                                                               'low': 'min',
                                                               'close': 'last',
                                                               'volume': 'sum'})
        # drop nan values
        regular_df.dropna(inplace=True)

        self.df_writer.save(regular_df, output_path)
        return True


# %% Run
import sys
sys.path.append('lib')

from lib.modules.drinfo.persistence.dataframe_writer import DataFrameWriter
from lib.modules.drinfo.persistence.price_csv_reader import PriceCsvReader

# Dependency Injection
writer = DataFrameWriter()
reader = PriceCsvReader()
parquet_reader = PriceParquetReader()

resampling_price_etl = ResamplingNqPrice(reader=parquet_reader, df_writer=writer)

# Executed tasks
# resampling_price_etl.process_task(timeframe='5T', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                   output_path='data/out/nq/NQ.ohlcv-5m.202109-202405.parquet')
# resampling_price_etl.process_task(timeframe='1T', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                   output_path='data/out/nq/NQ.ohlcv-1m.202109-202405.parquet')
# resampling_price_etl.process_task(timeframe='15S', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                   output_path='data/out/nq/NQ.ohlcv-15s.202109-202405.parquet')
# resampling_price_etl.process_task(timeframe='5S', input_path='data/out/nq/NQ.ohlcv-1s.202109-202405.parquet',
#                   output_path='data/out/nq/NQ.ohlcv-5s.202109-202405.parquet')
# resampling_price_etl.sample_data_task(timeframe='5T', input_path='data/out/nq/NQ.ohlcv-1s.202109-202405.parquet',
#                   output_path='data/out/nq/NQ.ohlcv-5m.202206-202208.sample.parquet')
# resampling_price_etl.sample_data_task(timeframe='1T', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                     output_path='data/out/nq/NQ.ohlcv-1m.202206-202208.sample.parquet')
# resampling_price_etl.sample_data_task(timeframe='15S', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                     output_path='data/out/nq/NQ.ohlcv-15s.202206-202208.sample.parquet')
# resampling_price_etl.sample_data_task(timeframe='5S', input_path='data/out/nq/NQ.ohlcv-1s.202109-202405.parquet',
#                   output_path='data/out/nq/NQ.ohlcv-5s.202206-202208.sample.parquet')
# resampling_price_etl.sample_data_task(timeframe='10T', input_path='data/in/NQ.ohlcv-1s.202109-202405-2.csv',
#                    output_path='data/out/nq/NQ.ohlcv-10m.202206-202208.sample.parquet'
print('Resampling Price Tasks completed!')
