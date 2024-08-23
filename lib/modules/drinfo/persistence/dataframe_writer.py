import pandas as pd


class DataFrameWriter:
    def __init__(self):
        pass

    def save(self, data: pd.DataFrame, path: str):
        data.to_parquet(path)
        print(f'File saved to {path}')