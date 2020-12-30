import math

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
        return max(ST-self.K, 0)

    def PriceByPath(self, path):
        payoff=0
        for i in range(len(path[-1])):
            payoff += self.payoff(path[-1][i])
        return payoff/len(path[-1])*math.exp(-self.r*(self.T-self.t)/252)                           # matching discouting method with divident?

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
        payoff=0
        for i in range(len(path[-1])):
            payoff_i = self.payoff(path[-1][i])
            if payoff_i>0 and max(path[:,i])<self.B:
                payoff += payoff_i
        return payoff/len(path[-1])*math.exp(-self.r*(self.T-self.t)/252)
