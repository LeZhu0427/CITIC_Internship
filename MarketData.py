import numpy as np
import math
from enum import Enum, unique, auto
from numpy.random import mtrand


@unique
class DividendType(Enum):
    ContinuousYield = auto()
    DiscreteCash = auto()
    DiscreteProp = auto()


class MarketData:
    def __init__(self, spot: float, vol: float, r: float):
        self.spot = spot
        self.vol = vol
        self.r = r
        self.q = 0.0
        self.d = None
        self.delta = None

    def reset_div(self):
        self.q = 0.0
        self.d = None
        self.delta = None

    def set_div(self, div_amount: any, div_type: DividendType):
        self.div_type = div_type
        if div_type == DividendType.ContinuousYield:
            self.q = div_amount
        elif div_type == DividendType.DiscreteCash:
            self.d = div_amount.copy()
        elif div_type == DividendType.DiscreteProp:
            self.delta = div_amount.copy()
        else:
            raise NotImplementedError
        # self.div_freq = div_freq

    def div_convert(self, div_amount: float, fr_type: DividendType, to_type: DividendType) -> float:
        if fr_type == to_type:
            return div_amount
        elif fr_type == DividendType.ContinuousYield and to_type == DividendType.DiscreteCash:
            raise NotImplementedError
        elif fr_type == DividendType.DiscreteProp and to_type == DividendType.DiscreteCash:
            # TODO: remove hard code
            return div_amount * self.spot * math.exp(self.r / 360 * 180)
        elif fr_type == DividendType.DiscreteProp and to_type == DividendType.ContinuousYield:
            # TODO: remove hard code
            return -math.log(1 - div_amount) / 360  # daily yield
