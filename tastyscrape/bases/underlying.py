from enum import Enum
import warnings


class UnderlyingType(Enum):
    EQUITY = 'Equity'
    FUTURE = 'Futures'
    INDEX  = 'Index'

class Underlying():
    def __init__(self, ticker: str, type: UnderlyingType):
        self.ticker = ticker
        self.type = type
        if(self.type != UnderlyingType.EQUITY):
            warnings.warn("Option related functions are currently only supported for Equity Options")
