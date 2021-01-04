import math
from scipy.stats import norm


class Option:
    def __init__(self, parameter_dict):
        self.K = parameter_dict['K']
        self.T = parameter_dict['T']
        self.t = parameter_dict['t']
        self.r = parameter_dict['r']  # annual interest rate


class EuropeanOption(Option):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)

    def payoff(self):
        pass


class EuropeanCall(EuropeanOption):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)

    def payoff(self, ST):
        return max(ST - self.K, 0)

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
        if self.K > 0:
            d1 = (math.log(S0 / self.K) + (self.r - q + 0.5 * vol * vol) * (self.T - self.t) / 360) / (
                        vol * math.sqrt((self.T - self.t) / 360))
            d2 = d1 - vol * math.sqrt((self.T - self.t) / 360)
            return S0 * norm.cdf(d1) - self.K * math.exp(-self.r * (self.T - self.t) / 360) * norm.cdf(d2)
        else:
            return S0 * math.exp(-sum(q) * (self.T - self.t) / 360)

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


class BarrierOption(Option):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)
        self.B = parameter_dict['B']  # barrier level

    def payoff(self):
        pass


class UpandOutCall(BarrierOption):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)

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
