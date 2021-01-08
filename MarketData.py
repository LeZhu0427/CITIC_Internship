import numpy as np
import math
from enum import Enum, unique, auto
from numpy.random import mtrand


@unique
class DividendType(Enum):
    ContinuousYield = auto()
    DiscreteCash = auto()
    DiscreteCash_m1 = auto()
    DiscreteCash_m2 = auto()
    DiscreteProp = auto()


class MarketData:
    def __init__(self, spot: float, vol: float, r: float):
        self.spot = spot
        self.vol = vol
        self.r = r
        self.q = 0.0
        self.d = None
        self.delta = None
        self.frequency = None

    def reset_div(self):
        self.q = 0.0
        self.d = None
        self.delta = None
        self.d_model1 = None
        self.d_model2 = None

    def set_div(self, div_amount: any, div_type: DividendType, frequency: int):
        self.div_type = div_type
        self.frequency = frequency
        if div_type == DividendType.ContinuousYield:
            self.q = div_amount
        elif div_type == DividendType.DiscreteCash:
            #self.d = div_amount.copy()
            self.d = div_amount
        elif div_type == DividendType.DiscreteCash_m1:
            self.d_model1 = div_amount
        elif div_type == DividendType.DiscreteCash_m2:
            self.d_model2 = div_amount
        elif div_type == DividendType.DiscreteProp:
            #self.delta = div_amount.copy()
            self.delta = div_amount
        else:
            raise NotImplementedError
        # self.div_freq = div_freq

    def div_convert(self, div_amount: float, frequency: int, fr_type: DividendType, to_type: DividendType) -> float:
        # frequency: number of payment per year
        # dividend_amount
        if frequency == 0:
            return 0.0
        if fr_type == to_type:
            return div_amount
        elif fr_type == DividendType.ContinuousYield and to_type == DividendType.DiscreteCash:
            raise NotImplementedError
        elif fr_type == DividendType.DiscreteProp and to_type in (DividendType.DiscreteCash,
                                                                   DividendType.DiscreteCash_m1,
                                                                   DividendType.DiscreteCash_m2):
            # same conversion for all cash dividend
            # TODO: remove hard code
            #return div_amount * self.spot * math.exp(self.r / 360 * 180)
            #dt = frequency/360
            #return div_amount/frequency * self.spot * math.exp(self.r * dt)
            return self.spot * (1 - pow(1 - div_amount/frequency, frequency)) / (1 - math.exp(-self.r*1)) * (math.exp(self.r/frequency)-1)
        elif fr_type == DividendType.DiscreteProp and to_type == DividendType.ContinuousYield:
            # TODO: remove hard code
            return - frequency * math.log(1 - div_amount/frequency) / 360
