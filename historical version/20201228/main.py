# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Option import *
from PricingModel import *
from Price import Price

parameter1 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "type": 'dividend yield', 'frequency': 252}    # annual dividend rate (compounded)
parameter2 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 1, "type": 'discrete cash dividend', 'frequency': 126}      # annual dividend amount, semi-annual dividend
parameter3 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "type": 'discrete proportional dividend', 'frequency': 126}    # annual dividend rate (proportional)
print("European call with divident yield : ", Price(EuropeanCall, parameter1, Monte_Carlo))
print("European call with discrete cash dividend: ", Price(EuropeanCall, parameter2, Monte_Carlo))
print("European call with discrete proportional dividend: ", Price(EuropeanCall, parameter3, Monte_Carlo))

parameter4 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "B": 130, "type": 'dividend yield', 'frequency': 252}    # annual dividend rate (compounded)
parameter5 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 1, "B": 130, "type": 'discrete cash dividend', 'frequency': 126}      # annual dividend amount, semi-annual dividend
parameter6 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': 0.01, "B": 130, "type": 'discrete proportional dividend', 'frequency': 126}    # annual dividend rate (proportional)
print("Up-and-out call with divident yield : ", Price(UpandOutCall, parameter4, Monte_Carlo))
print("Up-and-out call with discrete cash dividend: ", Price(UpandOutCall, parameter5, Monte_Carlo))
print("Up-and-out call with discrete proportional dividend: ", Price(UpandOutCall, parameter6, Monte_Carlo))


