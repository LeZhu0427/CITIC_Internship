import math
from scipy.stats import norm
from dataclasses import dataclass
from MarketData import MarketData
from enum import Enum, unique, auto


@unique
class OptionType(Enum):
    Forward = auto()
    European = auto()
    UpandOutCall = auto()


@dataclass(frozen=True)
class Option:
    K: float
    T: float
    t: float
    cp: float

    @staticmethod
    def option_type():
        pass

    def payoff(self, ST: float):
        pass

    def PriceByPath(self, path: dict):
        pass

    def PriceByBS(self, market: MarketData):
        pass


@dataclass(frozen=True)
class EuropeanOption(Option):

    @staticmethod
    def option_type():
        return OptionType.European.name

    @classmethod
    def create(cls, param: dict):
        return cls(K=param['K'], T=param['T'], t=param['t'], cp=1.0)

    def payoff(self, ST: float):
        return max(self.cp * (ST - self.K), 0.0)

    def PriceByPath(self, path_variable: dict):
        payoff = 0
        for i in range(len(path_variable['path'])):
            payoff += self.payoff(path_variable['path'][i])
        return payoff / len(path_variable['path']) * path_variable['df']

    def PriceByBS(self, market: MarketData):
        year_frac = (self.T - self.t) / 360.0
        fwd = market.spot * math.exp((market.r - market.q) * year_frac)
        df = math.exp(- market.r * year_frac)
        return EuropeanOption.Black73(cp=self.cp, fwd=fwd, strk=self.K, vol=market.vol, year_frac=year_frac, df=df)

    @staticmethod
    def Black73(cp: float = 1.0, fwd: float = 1.0, strk: float = 1.0, vol: float = 1.0, year_frac=1.0,
                df: float = 1.0) -> float:
        """Black Scholes Closed Form"""
        if year_frac <= 1.0e-8:
            fv = max(0.0, cp * (fwd - strk))
        elif strk <= 1.0e-8:
            fv = max(0.0, cp * (fwd - strk))
        else:
            vol = max(1.0e-8, vol)
            var_sqrt = vol * math.sqrt(year_frac)
            d1 = math.log(fwd / strk) / var_sqrt + 0.5 * var_sqrt
            d2 = d1 - var_sqrt
            fv = cp * (fwd * norm.cdf(cp * d1) - strk * norm.cdf(cp * d2))
        return fv * df


@dataclass(frozen=True)
class Forward(EuropeanOption):

    @staticmethod
    def option_type():
        return OptionType.Forward.name

@dataclass(frozen=True)
class BarrierOption(Option):
    B: float

    @classmethod
    def create(cls, param: dict):
        return cls(K=param['K'], T=param['T'], t=param['t'], cp=1.0, B=param['B'])


@dataclass(frozen=True)
class UpandOutCall(BarrierOption):

    @staticmethod
    def option_type():
        return OptionType.UpandOutCall.name

    def payoff(self, ST: float):
        return max(ST - self.K, 0.0)

    def PriceByPath(self, path_variable: dict):
        '''payoff=0
        for i in range(len(path[-1])):
            payoff_i = self.payoff(path[-1][i])
            if payoff_i>0 and max(path[:,i])<self.B:
                payoff += payoff_i
        return payoff/len(path[-1])*math.exp(-self.r*(self.T-self.t)/252)'''
        payoff = 0
        for i in range(len(path_variable['path'])):
            payoff += self.payoff(path_variable['path'][i])
        return payoff / len(path_variable['path']) * path_variable['df']
