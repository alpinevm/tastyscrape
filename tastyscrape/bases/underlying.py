from enum import Enum


class UnderlyingType(Enum):
    EQUITY = 'Equity'
    FUTURE = 'Futures'
    INDEX  = 'Index'

class Underlying():
    def __init__(self, ticker=None):
        self.ticker = ticker
