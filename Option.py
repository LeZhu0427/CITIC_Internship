import math
from scipy.stats import norm
from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    K: float
    T: float
    t: float
    cp: float
    r: float  # annual interest rate

    def payoff(self, ST: float):
        pass


@dataclass(frozen=True)
class EuropeanOption(Option):

    @classmethod
    def create(cls, param: dict):
        return cls(K=param['K'], T=param['T'], t=param['t'], r=param['r'], cp=1.0)

    def payoff(self, ST: float):
        return max(self.cp * (ST - self.K), 0.0)

    def PriceByPath(self, path):
        payoff = 0
        for i in range(len(path)):
            payoff += self.payoff(path[i])
        return payoff / len(path) * math.exp(
            -self.r * (self.T - self.t) / 252)  # matching discouting method with divident?

    def PriceByBS(self, parameter_dict):
        S0 = parameter_dict['S0']
        q = parameter_dict['dividend']
        vol = parameter_dict['vol']
        year_frac = (self.T - self.t) / 360.0
        fwd = S0 * math.exp((self.r - q) * year_frac)
        df = math.exp(- self.r * year_frac)
        return EuropeanOption.Black73(cp=self.cp, fwd=fwd, strk=self.K, vol=vol, year_frac=year_frac, df=df)

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
class BarrierOption(Option):
    B: float

    @classmethod
    def create(cls, param: dict):
        return cls(K=param['K'], T=param['T'], t=param['t'], cp=1.0, r=param['r'], B=param['B'])


@dataclass(frozen=True)
class UpandOutCall(BarrierOption):

    def payoff(self, ST):
        return max(ST - self.K, 0)

    def PriceByPath(self, path):
        '''payoff=0
        for i in range(len(path[-1])):
            payoff_i = self.payoff(path[-1][i])
            if payoff_i>0 and max(path[:,i])<self.B:
                payoff += payoff_i
        return payoff/len(path[-1])*math.exp(-self.r*(self.T-self.t)/252)'''
        payoff = 0
        for i in range(len(path)):
            payoff += self.payoff(path[i])
        return payoff / len(path) * math.exp(-self.r * (self.T - self.t) / 252)
