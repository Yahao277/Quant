import numpy as np
import pandas as pd

# %%
datapath = 'data/ES/glbx-mdp3-20170601.ohlcv-1m.csv'
df = pd.read_csv(datapath, index_col='ts_event')
df

# %%
class Main:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')

    def greet(self, other_name):
        print(f'Hello, {other_name}, my name is {self.name}.')


class DataService:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')

    def greet(self, other_name):
        print(f'Hello, {other_name}, my name is {self.name}.')

class DataAnalyzer:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')

    def greet(self, other_name):
        print(f'Hello, {other_name}, my name is {self.name}.')

class StrategySetup:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')

    def greet(self, other_name):
        print(f'Hello, {other_name}, my name is {self.name}.')
