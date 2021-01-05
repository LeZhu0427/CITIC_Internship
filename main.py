# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Option import *
from PricingModel import *
from Price import Price
from MarketData import MarketData, DividendType

import matplotlib.pyplot as plt

S0 = 100
vol = 0.1
r = 0.01
market = MarketData(spot=S0, vol=vol, r=r)
delta = 0.01
# TODO: this div amount is inconsistent with the rest
market.set_div(div_amount=0.01, div_type=DividendType.ContinuousYield)

K = 100
T = 360
t = 0
option = EuropeanOption(K=K, T=T, t=t, cp=1)
forward = Forward(K=0.0, T=T, t=t, cp=1)
n_path = 100000
model = MonteCarlo(n_path, t, T)

Price(option, market, Analytic())
market.reset_div()
dividend1 = market.div_convert(div_amount=delta, fr_type=DividendType.DiscreteProp,
                               to_type=DividendType.ContinuousYield)
market.set_div(div_amount=dividend1, div_type=DividendType.ContinuousYield)
Price(option, market, model)
Price(forward, market, model)

market.reset_div()
d = market.div_convert(div_amount=delta, fr_type=DividendType.DiscreteProp, to_type=DividendType.DiscreteCash)
dividend2 = np.zeros(360)
dividend2[179] = d  # d = S0*e^(rt)*delta
market.set_div(div_amount=dividend2, div_type=DividendType.DiscreteCash)
Price(option, market, model)
Price(forward, market, model)

market.reset_div()
dividend3 = np.zeros(360)
dividend3[179] = delta
market.set_div(div_amount=dividend3, div_type=DividendType.DiscreteProp)
Price(option, market, model)
Price(forward, market, model)


# compare ATM European call in 3 dividends
'''dividend_yield=[]
cash_dividend=[]
proportional_dividend=[]
for i in range(10):
    model = Monte_Carlo(n_path, t, T)
    dividend_yield.append(Price(EuropeanOption, parameter1, model))
    cash_dividend.append(Price(EuropeanOption, parameter2, model))
    proportional_dividend.append(Price(EuropeanOption, parameter3, model))
print(dividend_yield)
print(cash_dividend)
print(proportional_dividend)
np.save('dividend_yield.npy',dividend_yield)
np.save('cash_dividend.npy',cash_dividend)
np.save('proportional_dividend.npy',proportional_dividend)'''
'''
[3.5185041097852836, 4.266686487515944, 3.7187056542625507, 3.9249722998030916, 4.02103191291618, 3.875374929919656, 3.5985177608681793, 3.509104025231723, 3.2987225916479375, 3.7781256088716235]
[3.53584422670298, 4.2884599458044175, 3.737630628467244, 3.9445852689972596, 4.041509661070356, 3.894441381521445, 3.6164796459644437, 3.526521218530505, 3.315318658524736, 3.796416929005649]
[3.51839988402595, 4.266559512887719, 3.7185947021463206, 3.9248556109400514, 4.020912421135638, 3.8752597134790467, 3.598410951485733, 3.5090002444470465, 3.2986249805040715, 3.7780136177820647]
'''

# TODO: update this part
# #
# frequency = [1,2,4,12,24,48,360]        # frequency n times per year
# dividend_yield_freq=[]
# cash_dividend_freq=[]
# proportional_dividend_freq=[]
#
# dividend_yield_forward=[]
# cash_dividend_forward=[]
# proportional_dividend_forward=[]
#
# delta_annual = 0.01
#
# model = MonteCarlo(n_path, t, T)
# for i in frequency:
#     delta = delta_annual/i
#     q = -i*math.log(1 - delta/i) / 360   # daily yield
#     d = delta * S0 * math.exp(r / i)
#
#     dividend1 = np.ones(360) * q
#     dividend2 = np.zeros(360)
#     dividend3 = np.zeros(360)
#
#     delta_t = 360//i
#     for j in range(i):
#         dividend2[(j+1)*delta_t-1] = d  # d = S0*e^(rt)*delta
#         dividend3[(j+1)*delta_t-1] = delta
#
#     parameter1 = {'S0': S0, 'K': K, 'T': T, 't': t, 'vol': vol, 'r': r, 'q': dividend1}  # annual dividend rate (compounded)
#     parameter11 = {'S0': S0, 'K': 0, 'T': T, 't': t, 'vol': vol, 'r': r, 'q': dividend1}  # annual dividend rate (compounded)
#     print('frequency: ',i)
#     C1 = Price(EuropeanOption, parameter1, model)
#     F1 = Price(EuropeanOption, parameter11, model)
#     print("European call with dividend yield : ", C1)
#     print("Forward with dividend yield : ", F1)
#
#
#     parameter2 = {'S0': S0, 'K': K, 'T': T, 't': t, 'vol': vol, 'r': r, 'd': dividend2}
#     parameter22 = {'S0': S0, 'K': 0, 'T': T, 't': t, 'vol': vol, 'r': r, 'd': dividend2}
#     C2 = Price(EuropeanOption, parameter2, model)
#     F2 = Price(EuropeanOption, parameter22, model)
#     print("European call with discrete cash dividend: ", C2)
#     print("Forward with discrete cash dividend: ", F2)
#
#
#     parameter3 = {'S0': S0, 'K': K, 'T': T, 't': t, 'vol': vol, 'r': r, 'delta': dividend3}
#     parameter33 = {'S0': S0, 'K': 0, 'T': T, 't': t, 'vol': vol, 'r': r, 'delta': dividend3}
#     C3 = Price(EuropeanOption, parameter3, model)
#     F3 = Price(EuropeanOption, parameter33, model)
#     print("European call with discrete proportional dividend: ", C3)
#     print("Forward with discrete proportional dividend: ", F3)
#     print()
#
#     dividend_yield_freq.append(C1)
#     cash_dividend_freq.append(C2)
#     proportional_dividend_freq.append(C3)
#
#     dividend_yield_forward.append(F1)
#     cash_dividend_forward.append(F2)
#     proportional_dividend_forward.append(F3)
#
# np.save('frequency.npy', frequency)
# np.save('dividend_yield_freq.npy', dividend_yield_freq)
# np.save('cash_dividend_freq.npy', cash_dividend_freq)
# np.save('proportional_dividend_freq.npy', proportional_dividend_freq)
# plt.plot(frequency, dividend_yield_freq, label='dividend_yield')
# plt.plot(frequency, cash_dividend_freq, label='cash_dividend')
# plt.plot(frequency, proportional_dividend_freq, label='proportional_dividend')
# plt.legend()
# plt.xlabel('dividend frequency')
# plt.ylabel('European call price')
# plt.savefig("frequency-price.png")
# plt.show()
#
# np.save('dividend_yield_forward.npy', dividend_yield_forward)
# np.save('cash_dividend_forward.npy', cash_dividend_forward)
# np.save('proportional_dividend_forward.npy', proportional_dividend_forward)
# plt.plot(frequency, dividend_yield_forward, label='dividend_yield_forward')
# plt.plot(frequency, cash_dividend_forward, label='cash_dividend_forward')
# plt.plot(frequency, proportional_dividend_forward, label='proportional_dividend_forward')
# plt.legend()
# plt.xlabel('dividend frequency')
# plt.ylabel('forward price')
# plt.savefig("frequency-forward.png")
# plt.show()
#
# print(dividend_yield_freq)
# print(cash_dividend_freq)
# print(proportional_dividend_freq)
# print(dividend_yield_forward)
# print(cash_dividend_forward)
# print(proportional_dividend_forward)
#
# '''
# [3.9424289966357033, 4.21623893697899, 4.356583873411636, 4.451563121902687, 4.4755012591324395, 4.487500311199823, 4.497915066989274]
# [3.9821585316279577, 3.973347544683029, 3.9690642989938034, 3.9661751823207125, 3.9654580005882045, 3.963575144635045, 3.964785179264228]
# [3.9423121816462143, 3.9436543081391044, 3.944322133738035, 3.9447661505682543, 3.9448770055844773, 3.9449324106370645, 3.944980416240857]
# [98.74000682693998, 99.23931153890233, 99.48825990282813, 99.6542823804078, 99.6958149169101, 99.71658671090817, 99.73459219479625]
# [98.74163909389061, 98.74371627899268, 98.74474141988416, 98.74543134184538, 98.74560311854385, 98.7452962614366, 98.74576387910702]
# [98.73998892467283, 98.742482358734, 98.74372284607735, 98.74454754618947, 98.74475343576603, 98.74485633781202, 98.74494549655148]
# '''