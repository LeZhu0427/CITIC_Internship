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
        #np.random.normalmtrand.RandomState(seed=42).randn(self.n_path, self.T - self.t)

    @staticmethod
    def model_type():
        return ModelType.MonteCarlo

    def generate_discrete_data(self):
        self.path = np.ones((1, self.n_path)) * self.S0  # row 0: S0
        self.ST = np.ones(self.n_path) * self.S0  # S0
        #self.Wt = np.random.normalmtrand.RandomState(seed=42).randn(self.n_path, self.T - self.t)
        self.Wt = np.random.normal(0, 1/math.sqrt(1/360), self.n_path*(self.T - self.t))

    def generate_ST(self, S0, vol, r, T, t, d, d_model1, d_model2, q, delta, frequency):
        # r is daily interest rate

        n_timestep = T - t
        q1 = np.ones(n_timestep) * q

        d1 = np.zeros(n_timestep)
        delta1 = np.zeros(n_timestep)
        ST = np.array([S0] * self.n_path)  # S0
        if frequency!=0:
            dt = 360//frequency
            if d is not None:
                for j in range(1,frequency+1):
                    d1[j*dt-1] = d
            elif delta is not None:
                for j in range(1,frequency+1):
                    delta1[j*dt-1] = delta / frequency
            elif d_model1 is not None:
                discount_PV = 0
                for j in range(1, frequency + 1):
                    discount_PV += math.exp(-r * j * dt)
                ST = np.array([S0 - d_model1 * discount_PV] * self.n_path)  # S0
            elif d_model2 is not None:
                dividend_FV = 0
                for j in range(1, frequency + 1):
                    #dividend_FV += math.exp(-r * (j + 1) * dt)
                    dividend_FV += math.exp(r * (1 - j * dt))
                dividend_FV = dividend_FV * d_model2 * math.exp(r * (T - t))

        for i in range(0, T - t):
            # i: time
            '''dS = ST * (np.ones(self.n_path) * (r - q1[i]) + vol * self.Wt[i:i + self.n_path]) - np.ones(self.n_path) * d1[
                i]  # daily increment'''
            dS = ST * (np.ones(self.n_path) * (r - q1[i]) + vol * self.Wt[i*self.n_path:(i+1)*self.n_path]) - np.ones(self.n_path) * \
                 d1[i]  # daily increment
            ST = (ST + dS) * (1 - delta1[i])  # discrete proportional dividend is paid at market close
            if min(ST) < 0:
                print("cash divident: S", i, "<0")  # it the stock price is negative after paying dividend
        # TODO: contradicting basis
        #df = math.exp(-r * 360 * (T - t) / 252)  # matching discouting method with dividend?
        df = math.exp(-r * (T - t))  # matching discouting method with dividend?
        if d_model2 is not None:
            return {'path': ST - np.ones(self.n_path)*dividend_FV, 'df': df}
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


'''
European ModelType.Analytic DividendType.ContinuousYield 3.9480822810875194
European ModelType.MonteCarlo DividendType.ContinuousYield 3.959361378665875
Forward ModelType.MonteCarlo DividendType.ContinuousYield 99.16408637756277
European ModelType.MonteCarlo DividendType.DiscreteCash 3.9992615484786818
Forward ModelType.MonteCarlo DividendType.DiscreteCash 99.16572565495483
European ModelType.MonteCarlo DividendType.DiscreteCash_m1 3.953843359835985
Forward ModelType.MonteCarlo DividendType.DiscreteCash_m1 99.15402967867253
European ModelType.MonteCarlo DividendType.DiscreteCash_m2 3.9992754116285134
Forward ModelType.MonteCarlo DividendType.DiscreteCash_m2 99.16575343234605
European ModelType.MonteCarlo DividendType.DiscreteProp 3.959244061966392
'''