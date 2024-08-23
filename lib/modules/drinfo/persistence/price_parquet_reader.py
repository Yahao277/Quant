import pandas as pd


class PriceParquetReader:
    def __init__(self):
        pass
    def read(self, file_path: str = 'data/out/nq/NQ.ohlcv-1s.202109-202405.parquet'):
        # Load sample data with ts_event as datetime index
        df = pd.read_parquet(file_path)
        return df
