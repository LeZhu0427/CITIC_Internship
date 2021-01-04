import numpy as np
import math
from numpy.random import mtrand


class PricingModel:
    def __init__(self, parameter_dict):
        self.n_path = 100000
        self.K = parameter_dict['K']
        self.T = parameter_dict['T']  # expire time (unit: days)
        self.t = parameter_dict['t']  # start time (unit: days)
        self.S0 = parameter_dict['S0']
        self.vol = parameter_dict['vol']
        self.r = parameter_dict['r'] / 360  # daily interest rate
        self.dividend = parameter_dict['dividend']
        self.frequency = parameter_dict['frequency']
        self.path = np.array([[self.S0] * self.n_path])  # row 0: S0
        np.random.seed(42)
        self.Wt = np.random.normal(0, self.vol / math.sqrt(360), self.n_path * (self.T - self.t))
        self.ST = np.array([self.S0] * self.n_path)
        self.if_barrier = 'B' in parameter_dict.keys()  # if it is a barrier option
        if self.if_barrier:
            self.B = parameter_dict['B']


class Monte_Carlo(PricingModel):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)

    # def plot_path(self):

    def generate_discrete_data(self):
        self.path = np.ones((1, self.n_path)) * self.S0  # row 0: S0
        self.ST = np.ones(self.n_path) * self.S0  # S0
        self.Wt = np.random.normalmtrand.RandomState(seed=42).randn(self.n_path, self.T - self.t)

    def generate_path_dividend_yield(self):
        self.ST = np.array([self.S0] * self.n_path)  # S0
        if_hit = np.ones(self.n_path)  # if barrier is hit
        for i in range(0, self.T - self.t):
            dS = self.ST * (np.ones(self.n_path) * (self.r - self.dividend[i]) + self.Wt[
                                                                                 i:i + self.n_path])  # daily increment
            self.ST = self.ST + dS
            if self.if_barrier:
                if_hit *= (self.ST < self.B)
        return self.ST * if_hit

    def generate_path_discrete_cash_dividend(self):
        self.ST = np.array([self.S0] * self.n_path)  # S0
        if_hit = np.ones(self.n_path)  # if barrier is hit
        for i in range(0, self.T - self.t):
            dS = self.ST * (np.ones(self.n_path) * self.r + self.Wt[i:i + self.n_path]) - np.ones(self.n_path) * \
                 self.dividend[i]
            self.ST = self.ST + dS
            if self.if_barrier:
                if_hit *= (self.ST < self.B)
            if min(self.ST) < 0:
                print("cash divident: S", i, "<0")
        return self.ST * if_hit

    def generate_path_discrete_proportional_dividend(self):
        self.ST = np.array([self.S0] * self.n_path)  # S0
        if_hit = np.ones(self.n_path)  # if barrier is hit
        for i in range(0, self.T - self.t):
            # self.ST = self.ST*(1-self.dividend[i])                             # dividend is paid at market opening
            dS = self.ST * (np.ones(self.n_path) * self.r + self.Wt[i:i + self.n_path])
            self.ST = (self.ST + dS) * (1 - self.dividend[i])  # dividend is paid at market close
            if self.if_barrier:
                if_hit *= (self.ST < self.B)
        return self.ST * if_hit
