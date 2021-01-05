import numpy as np
import math
from enum import Enum, unique, auto
from numpy.random import mtrand


@unique
class ModelType(Enum):
    Analytic = auto()
    MonteCarlo = auto()


class PricingModel:
    @staticmethod
    def model_type():
        pass

    def generate_ST(self, **kwargs):
        pass

    '''self.n_path = 100000
    self.T = parameter_dict['T']  # expire time (unit: days)
    self.t = parameter_dict['t']  # start time (unit: days)
    self.S0 = parameter_dict['S0']
    self.vol = parameter_dict['vol']
    self.r = parameter_dict['r'] / 360  # daily interest rate
    self.dividend = parameter_dict['dividend']
    self.frequency = parameter_dict['frequency']
    self.path = np.array([[self.S0] * self.n_path])  # row 0: S0
    np.random.seed(42)
    self.Wt = np.random.normal(0, 1/math.sqrt(360), self.n_path * (self.T - self.t))     # common random numbers, size: self.n_path * _time_step
    self.ST = np.array([self.S0] * self.n_path)
    self.if_barrier = 'B' in parameter_dict.keys()  # if it is a barrier option
    if self.if_barrier:
        self.B = parameter_dict['B']'''


class Analytic(PricingModel):
    @staticmethod
    def model_type():
        return ModelType.Analytic


class MonteCarlo(PricingModel):
    def __init__(self, n_path, t, T):
        self.n_path = n_path
        np.random.seed(42)
        self.Wt = np.random.normal(0, 1 / math.sqrt(360),
                                   n_path * (T - t))  # common random numbers, size: self.n_path * _time_step

    @staticmethod
    def model_type():
        return ModelType.MonteCarlo

    # def generate_discrete_data(self):
    #     self.path = np.ones((1, self.n_path)) * self.S0  # row 0: S0
    #     self.ST = np.ones(self.n_path) * self.S0  # S0
    #     self.Wt = np.random.normalmtrand.RandomState(seed=42).randn(self.n_path, self.T - self.t)

    def generate_ST(self, S0, vol, r, T, t, d, q, delta):
        n_timestep = T - t
        q = np.ones(n_timestep) * q
        if d is None:
            d = np.zeros(n_timestep)
        if delta is None:
            delta = np.zeros(n_timestep)

        ST = np.array([S0] * self.n_path)  # S0
        for i in range(0, T - t):
            dS = ST * (np.ones(self.n_path) * (r - q[i]) + vol * self.Wt[i:i + self.n_path]) - np.ones(self.n_path) * d[
                i]  # daily increment
            ST = (ST + dS) * (1 - delta[i])  # discrete proportional dividend is paid at market close
            if min(ST) < 0:
                print("cash divident: S", i, "<0")  # it the stock price is negative after paying dividend
        # TODO: contradicting basis
        df = math.exp(-r * 360 * (T - t) / 252)  # matching discouting method with divident?
        return {'path': ST, 'df': df}

    '''def generate_path_dividend_yield(self):
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
        return self.ST * if_hit'''
