import numpy as np
import pandas as pd
import sys
sys.path.append('lib')
from date_utils import is_edt
from services.session_service import SessionService

# %%
# if main run this
if __name__ == '__main__':
    print('hello')

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
