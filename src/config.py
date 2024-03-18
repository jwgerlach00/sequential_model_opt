import random


class Config:
    def __init__(self):
        self.k = 1
        self.m = 2

        self.seed = 31210
        random.seed(self.seed)

        self.budget0 = 4
        self.budget = 1


config = Config()
