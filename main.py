# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Option import *
from PricingModel import *
from Price import Price

delta = 0.01
d = delta * 100 * math.exp(0.01 / 360 * 180)
q = -math.log(1 - delta) / 360

print("European call")
divdend1 = np.ones(360) * q
parameter1 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend1,
              "type": 'dividend yield', 'frequency': 252}  # annual dividend rate (compounded)
parameter11 = {'S0': 100, 'K': 0, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend1,
               "type": 'dividend yield', 'frequency': 252}  # annual dividend rate (compounded)
print("European call with dividend yield : ", Price(EuropeanCall, parameter1, Monte_Carlo))
print("Forward with dividend yield : ", Price(EuropeanCall, parameter11, Monte_Carlo))

divdend2 = np.zeros(360)
divdend2[179] = d  # d = S0*e^(rt)*delta
parameter2 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend2,
              "type": 'discrete cash dividend', 'frequency': 252}  # annual dividend rate (compounded)
parameter22 = {'S0': 100, 'K': 0, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend2,
               "type": 'discrete cash dividend', 'frequency': 252}  # annual dividend rate (compounded)
print("European call with discrete cash dividend: ", Price(EuropeanCall, parameter2, Monte_Carlo))
print("Forward with discrete cash dividend: ", Price(EuropeanCall, parameter22, Monte_Carlo))

divdend3 = np.zeros(360)
divdend3[179] = delta
parameter3 = {'S0': 100, 'K': 100, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend3,
              "type": 'discrete proportional dividend', 'frequency': 252}  # annual dividend rate (proportional)
parameter33 = {'S0': 100, 'K': 0, 'T': 360, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend3,
               "type": 'discrete proportional dividend', 'frequency': 252}  # annual dividend rate (proportional)
print("European call with discrete proportional dividend: ", Price(EuropeanCall, parameter3, Monte_Carlo))
print("Forward with discrete proportional dividend: ", Price(EuropeanCall, parameter33, Monte_Carlo))

'''
self.n_path = 100000
K = 0
European call with dividend yield :  98.74000682693998
European call with discrete cash dividend:  98.7408272726391
European call with discrete proportional dividend:  98.73998892467283

self.n_path = 100000
K = 0
European call with dividend yield :  98.28392379028341
European call with discrete cash dividend:  98.28246655788503
European call with discrete proportional dividend:  98.28391813910402

self.n_path = 100000
K = 100
European call with dividend yield :  3.9424289966357025
European call with discrete cash dividend:  3.9620892474244096
European call with discrete proportional dividend:  3.9423121816462126
'''

divdend4 = np.ones(360) * q
divdend5 = np.zeros(360)
divdend5[179] = d  # d = S0*e^(rt)*delta
divdend6 = np.zeros(360)
divdend6[179] = delta
parameter4 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend4, "B": 130,
              "type": 'dividend yield', 'frequency': 252}  # annual dividend rate (compounded)
parameter5 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend5, "B": 130,
              "type": 'discrete cash dividend', 'frequency': 126}  # annual dividend amount, semi-annual dividend
parameter6 = {'S0': 100, 'K': 100, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend6, "B": 130,
              "type": 'discrete proportional dividend', 'frequency': 126}  # annual dividend rate (proportional)
parameter44 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend4, "B": 130,
               "type": 'dividend yield', 'frequency': 252}  # annual dividend rate (compounded)
parameter55 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend5, "B": 130,
               "type": 'discrete cash dividend', 'frequency': 126}  # annual dividend amount, semi-annual dividend
parameter66 = {'S0': 100, 'K': 0, 'T': 252, 't': 0, 'vol': 0.1, 'r': 0.01, 'dividend': divdend6, "B": 130,
               "type": 'discrete proportional dividend', 'frequency': 126}  # annual dividend rate (proportional)
print()
print('Up-and-out call')
print("Up-and-out call with dividend yield : ", Price(UpandOutCall, parameter4, Monte_Carlo))
# print("Forward with dividend yield : ", Price(UpandOutCall, parameter44, Monte_Carlo))
print("Up-and-out call with discrete cash dividend: ", Price(UpandOutCall, parameter5, Monte_Carlo))
# print("Forward with discrete cash dividend: ", Price(UpandOutCall, parameter55, Monte_Carlo))
print("Up-and-out call with discrete proportional dividend: ", Price(UpandOutCall, parameter6, Monte_Carlo))
# print("Forward with discrete proportional dividend: ", Price(UpandOutCall, parameter66, Monte_Carlo))

'''
European call
European call with dividend yield :  3.9424289966357025
Forward with dividend yield :  98.74000682693998
European call with discrete cash dividend:  3.9620892474244096
Forward with discrete cash dividend:  98.7408272726391
European call with discrete proportional dividend:  3.9423121816462126
Forward with discrete proportional dividend:  98.73998892467283

Up-and-out call
Up-and-out call with dividend yield :  3.2965850810146686
Up-and-out call with discrete cash dividend:  3.1642457994218516
Up-and-out call with discrete proportional dividend:  3.1419595492189965

Process finished with exit code 0
'''
