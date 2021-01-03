# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Option import *
from PricingModel import *
from Price import Price

'''parameter4 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "B": 130, "type": 'dividend yield', 'frequency': 252}    # annual dividend rate (compounded)
parameter5 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 1, "B": 130, "type": 'discrete cash dividend', 'frequency': 126}      # annual dividend amount, semi-annual dividend
parameter6 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "B": 130, "type": 'discrete proportional dividend', 'frequency': 126}    # annual dividend rate (proportional)
print("Up-and-out call with divident yield : ", Price(UpandOutCall, parameter4, Monte_Carlo))
print("Up-and-out call with discrete cash dividend: ", Price(UpandOutCall, parameter5, Monte_Carlo))
print("Up-and-out call with discrete proportional dividend: ", Price(UpandOutCall, parameter6, Monte_Carlo))'''

delta = 0.01
d = delta*100*math.exp(0.01/360*180)
q = -math.log(1-delta)/360

divdend = np.ones(360)*q
parameter1 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend, "type": 'dividend yield', 'frequency': 252}    # annual dividend rate (compounded)
print("European call with dividend yield : ", Price(EuropeanCall, parameter1, Monte_Carlo))

divdend = np.zeros(360)
divdend[179] = d   # d = S0*e^(rt)*delta
parameter2 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend, "type": 'discrete cash dividend', 'frequency': 252}    # annual dividend rate (compounded)
print("European call with discrete cash dividend: ", Price(EuropeanCall, parameter2, Monte_Carlo))

divdend = np.zeros(360)
divdend[179] = delta
parameter3 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend, "type": 'discrete proportional dividend', 'frequency': 252}    # annual dividend rate (proportional)
print("European call with discrete proportional dividend: ", Price(EuropeanCall, parameter3, Monte_Carlo))

'''
self.n_path = 100000
K = 0
European call with divident yield :  98.74000682693998
European call with discrete cash dividend:  98.7408272726391
European call with discrete proportional dividend:  98.73998892467283

self.n_path = 100000
K = 0
European call with divident yield :  98.28392379028341
European call with discrete cash dividend:  98.28246655788503
European call with discrete proportional dividend:  98.28391813910402

self.n_path = 100000
K = 100
European call with divident yield :  3.9424289966357025
European call with discrete cash dividend:  3.9620892474244096
European call with discrete proportional dividend:  3.9423121816462126
'''
