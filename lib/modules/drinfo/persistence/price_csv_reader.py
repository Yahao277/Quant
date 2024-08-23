import csv

import pandas as pd


class PriceCsvReader:
    def __init__(self):
        pass
    def read(self, file_path: str = 'data/out/ES.ohlcv-1m.sample.csv'):
        # Load sample data with ts_event as datetime index
        df = pd.read_csv(file_path, index_col='ts_event', parse_dates=True)
        return df
