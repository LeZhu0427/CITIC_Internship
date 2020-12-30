import numpy as np
import math

class PricingModel:
    def __init__(self, parameter_dict):
        self.n_path = 100000
        self.K = parameter_dict['K']
        self.T = parameter_dict['T']             #expire time (unit: days)
        self.t = parameter_dict['t']             #start time (unit: days)
        self.S0 = parameter_dict['S0']
        self.vol = parameter_dict['vol']
        self.r = parameter_dict['r']
        self.dividend = parameter_dict['dividend']
        self.frequency = parameter_dict['frequency']
        self.path = np.array([[self.S0]*self.n_path])         # row 0: S0

    def path(self):
        pass

class Monte_Carlo(PricingModel):
    def __init__(self, parameter_dict):
        super().__init__(parameter_dict)

    #def plot_path(self):

    def generate_path_dividend_yield(self):
        # constant vol, r, dividend
        self.path = np.array([[self.S0] * self.n_path])  # row 0: S0
        if type(self.vol)==int or type(self.vol)==float:
            vol = self.vol / math.sqrt(252)                     # convert annual vol to daily vol
            r = self.r/252                                      # convert annual interest rate to daily interest rate
            dividend = self.dividend/252                        # convert annual dividend to daily divident
            for i in range(self.t+1, self.T+1):
                Si = np.array([np.random.lognormal(0, vol*math.sqrt((i-self.t)), self.n_path)*self.S0*math.exp((r-dividend-0.5*vol*vol)*(i-self.t))])     # row i: Si
                self.path = np.r_[self.path, Si]                            # unnecessary copy?
        # array for vol, r, dividend
        else:
            for i in range(self.t+1, self.T+1):
                vol = self.vol   # array
                r = self.r # array
                dividend = self.dividend  # array
                Si = np.array([np.random.lognormal(0, vol[i]*math.sqrt((i-self.t)), self.n_path)*self.S0*math.exp((r[i]-dividend[i]-0.5*vol[i]*vol[i])*(i-self.t))])     # row i: Si
                self.path = np.r_[self.path, Si]
        return self.path

    def generate_path_discrete_cash_dividend(self):
        self.path = np.array([[self.S0] * self.n_path])  # row 0: S0
        # constant vol, r, dividend
        if type(self.vol) == int or type(self.vol) == float:
            vol = self.vol / math.sqrt(252)                     # convert annual vol to daily vol
            r = self.r / 252
            dividend = self.dividend / self.frequency           # cash dividend amount for each dividend payment day
            for i in range(self.t + 1, self.T + 1):
                # dividend paying day
                # fixed dividend paying day?  (i-self.t )%self.frequency==0
                if i%self.frequency==0:
                    dS = self.path[-1]*(np.random.normal(0, vol , self.n_path)+np.ones(self.n_path)*r) - np.ones(self.n_path)*dividend          # daily increment
                # non dividend paying day
                else:
                    dS = self.path[-1]*(np.random.normal(0, vol , self.n_path)+np.ones(self.n_path)*r)             # daily increment
                self.path = np.r_[self.path, np.array([dS+self.path[-1]])]
        return self.path

    def generate_path_discrete_proportional_dividend(self):
        self.path = np.array([[self.S0] * self.n_path])  # row 0: S0
        if type(self.vol) == int or type(self.vol) == float:
            vol = self.vol / math.sqrt(252)  # convert annual vol to daily vol
            r = self.r / 252
            dividend = self.dividend / self.frequency  # dividend percentage for each dividend payment day
            for i in range(self.t + 1, self.T + 1):
                # dividend paying day
                # fixed dividend paying day?  (i-self.t )%self.frequency==0
                dS = self.path[-1] * (np.random.normal(0, vol, self.n_path) + np.ones(self.n_path) * r)  # daily increment
                if i % self.frequency == 0:
                    # dividend paid at open
                    #dS = self.path[-1] * (np.random.normal(0, vol, self.n_path) + np.ones(self.n_path) * r) - self.path[-1] * dividend  # daily increment
                    # dividend paid at close
                    self.path = np.r_[self.path, np.array([dS + self.path[-1]])]
                    self.path[-1] = (1-dividend)*self.path[-1]
                # non dividend paying day
                else:
                    #dS = self.path[-1] * (np.random.normal(0, vol, self.n_path) + np.ones(self.n_path) * r)  # daily increment
                    self.path = np.r_[self.path, np.array([dS + self.path[-1]])]
        return self.path


