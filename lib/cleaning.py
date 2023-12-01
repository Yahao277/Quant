import pandas as pd

'''
timeframe naming convention: '1T', '15T', '5T', '1H', etc.
expected df: having timestamp as index, having columns: open, high, low, close, (volume)
'''


def resample(df: pd.DataFrame, timeframe: str):
    return df.resample(timeframe).agg({'open': 'first',
                                       'high': 'max',
                                       'low': 'min',
                                       'close': 'last',
                                       'volume': 'sum'})


'''
Cleaning data extracted from Databento ES futures data
'''


def cleaning(datapath: str = '../data/ES/glbx-mdp3-20170601.ohlcv-1m.csv'):
    df = pd.read_csv(datapath, index_col='ts_event')
    df.index = pd.to_datetime(df.index, unit='ns')

    # convert price from unit with 10^9 (with 9 decimals) to unit with 4165.25 (with 2 decimals)
    price_columns = ['open', 'high', 'low', 'close']
    df[price_columns] = df[price_columns].apply(lambda x: x / 10 ** 9)

    # filter out instrument_id = 9006
    filtered_df = df[df['instrument_id'] == 9006]

    # resample to 5 minutes
    resampled_df = filtered_df.resample('5T').agg({'open': 'first',
                                                   'high': 'max',
                                                   'low': 'min',
                                                   'close': 'last',
                                                   'volume': 'sum'})
    return resampled_df
