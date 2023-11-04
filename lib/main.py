class Main:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f'Hello, {self.name}!')

    def greet(self, other_name):
        print(f'Hello, {other_name}, my name is {self.name}.')
