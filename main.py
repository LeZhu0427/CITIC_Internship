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
market.set_div(div_amount=0.01, frequency=180, div_type=DividendType.ContinuousYield)

K = 100
T = 360
t = 0
option = EuropeanOption(K=K, T=T, t=t, cp=1)
forward = Forward(K=0.0, T=T, t=t, cp=1)

n_path = 100000
model = MonteCarlo(n_path, t, T)

Price(option, market, Analytic())

# dividend yield
market.reset_div()
dividend1 = market.div_convert(div_amount=delta, frequency=1, fr_type=DividendType.DiscreteProp,
                               to_type=DividendType.ContinuousYield)
market.set_div(div_amount=dividend1, frequency=1, div_type=DividendType.ContinuousYield)
Price(option, market, model)
Price(forward, market, model)

# discrete cash
market.reset_div()
d = market.div_convert(div_amount=delta, frequency=1, fr_type=DividendType.DiscreteProp, to_type=DividendType.DiscreteCash)
market.set_div(div_amount=d, frequency=1, div_type=DividendType.DiscreteCash)
Price(option, market, model)
Price(forward, market, model)

# discrete cash model 1
market.reset_div()
d = market.div_convert(div_amount=delta, frequency=1, fr_type=DividendType.DiscreteProp, to_type=DividendType.DiscreteCash_m1)
market.set_div(div_amount=d, frequency=1, div_type=DividendType.DiscreteCash_m1)
Price(option, market, model)
Price(forward, market, model)

# discrete cash model 2
market.reset_div()
d = market.div_convert(div_amount=delta, frequency=1, fr_type=DividendType.DiscreteProp, to_type=DividendType.DiscreteCash_m2)
market.set_div(div_amount=d, frequency=1, div_type=DividendType.DiscreteCash_m2)
Price(option, market, model)
Price(forward, market, model)

# discrete proportional
market.reset_div()
market.set_div(div_amount=delta, frequency=1, div_type=DividendType.DiscreteProp)
Price(option, market, model)
Price(forward, market, model)

# compare ATM European call in 3 dividends
# TODO: update this part
frequency = [1,2,4,12,24,180,360]     # frequency n times per year
dividend_yield_freq=[]
cash_dividend_freq=[]
proportional_dividend_freq=[]
cash_dividend_m1_freq=[]
cash_dividend_m2_freq=[]

dividend_yield_forward=[]
cash_dividend_forward=[]
proportional_dividend_forward=[]
cash_dividend_m1_forward=[]
cash_dividend_m2_forward=[]

delta_annual = 0.01
K = 100
T = 360
t = 0
n_path = 100000

for i in frequency:
    print('frequency: ', i)
    #delta_annual = 0.01/i

    market.set_div(div_amount=delta_annual, frequency=180, div_type=DividendType.ContinuousYield)

    option = EuropeanOption(K=K, T=T, t=t, cp=1)
    forward = Forward(K=0.0, T=T, t=t, cp=1)
    model = MonteCarlo(n_path, t, T)

    Price(option, market, Analytic())
    market.reset_div()
    dividend1 = market.div_convert(div_amount=delta_annual, frequency=i, fr_type=DividendType.DiscreteProp,
                                   to_type=DividendType.ContinuousYield)
    market.set_div(div_amount=dividend1, frequency=i, div_type=DividendType.ContinuousYield)
    C1 = Price(option, market, model)
    F1 = Price(forward, market, model)

    market.reset_div()
    d = market.div_convert(div_amount=delta, frequency=i, fr_type=DividendType.DiscreteProp,
                           to_type=DividendType.DiscreteCash)
    market.set_div(div_amount=d, frequency=i, div_type=DividendType.DiscreteCash)
    C2 = Price(option, market, model)
    F2 = Price(forward, market, model)

    # discrete cash model 1
    market.reset_div()
    d = market.div_convert(div_amount=delta, frequency=i, fr_type=DividendType.DiscreteProp,
                           to_type=DividendType.DiscreteCash_m1)
    market.set_div(div_amount=d, frequency=i, div_type=DividendType.DiscreteCash_m1)
    C21 = Price(option, market, model)
    F21 = Price(forward, market, model)

    # discrete cash model 2
    market.reset_div()
    d = market.div_convert(div_amount=delta, frequency=i, fr_type=DividendType.DiscreteProp,
                           to_type=DividendType.DiscreteCash_m2)
    market.set_div(div_amount=d, frequency=i, div_type=DividendType.DiscreteCash_m2)
    C22 = Price(option, market, model)
    F22 = Price(forward, market, model)

    market.reset_div()
    market.set_div(div_amount=delta, frequency=i, div_type=DividendType.DiscreteProp)
    C3 = Price(option, market, model)
    F3 = Price(forward, market, model)

    print()

    dividend_yield_freq.append(C1)
    cash_dividend_freq.append(C2)
    cash_dividend_m1_freq.append(C21)
    cash_dividend_m2_freq.append(C22)
    proportional_dividend_freq.append(C3)

    dividend_yield_forward.append(F1)
    cash_dividend_forward.append(F2)
    cash_dividend_m1_forward.append(F21)
    cash_dividend_m2_forward.append(F22)
    proportional_dividend_forward.append(F3)

np.save('./results/frequency.npy', frequency)
np.save('./results/dividend_yield_freq.npy', dividend_yield_freq)
np.save('./results/cash_dividend_freq.npy', cash_dividend_freq)
np.save('./results/cash_dividend_m1_freq.npy', cash_dividend_freq)
np.save('./results/cash_dividend_m2_freq.npy', cash_dividend_freq)
np.save('./results/proportional_dividend_freq.npy', proportional_dividend_freq)

#plt.axis([-1,370,3,6])
plt.plot(frequency, dividend_yield_freq, label='dividend_yield')
plt.plot(frequency, cash_dividend_freq, label='cash_dividend')
#plt.plot(frequency, cash_dividend_m1_freq, label='cash_dividend_m1')
#plt.plot(frequency, cash_dividend_m2_freq, label='cash_dividend_m2')
plt.plot(frequency, proportional_dividend_freq, label='proportional_dividend')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('European call price')
plt.savefig("./results/frequency-price.png")
plt.show()

np.save('./results/dividend_yield_forward.npy', dividend_yield_forward)
np.save('./results/cash_dividend_forward.npy', cash_dividend_forward)
np.save('./results/cash_dividend_m1_forward.npy', cash_dividend_m1_forward)
np.save('./results/cash_dividend_m2_forward.npy', cash_dividend_m2_forward)
np.save('./results/proportional_dividend_forward.npy', proportional_dividend_forward)

#plt.axis([-1,370,95,105])
plt.plot(frequency, dividend_yield_forward, label='dividend_yield_forward')
plt.plot(frequency, cash_dividend_forward, label='cash_dividend_forward')
#plt.plot(frequency, cash_dividend_m1_forward, label='cash_dividend_m1_forward')
#plt.plot(frequency, cash_dividend_m2_forward, label='cash_dividend_m2_forward')
plt.plot(frequency, proportional_dividend_forward, label='proportional_dividend_forward')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('forward price')
plt.savefig("./results/frequency-forward.png")
plt.show()


plt.plot(frequency, cash_dividend_freq, label='cash_dividend')
plt.plot(frequency, cash_dividend_m1_freq, label='cash_dividend_m1')
plt.plot(frequency, cash_dividend_m2_freq, label='cash_dividend_m2')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('European call price (cash dividend)')
plt.savefig("./results/frequency-price_cash.png")
plt.show()

plt.plot(frequency, cash_dividend_forward, label='cash_dividend_forward')
plt.plot(frequency, cash_dividend_m1_forward, label='cash_dividend_m1_forward')
plt.plot(frequency, cash_dividend_m2_forward, label='cash_dividend_m2_forward')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('forward price (cash dividend)')
plt.savefig("./results/frequency-forward_cash.png")
plt.show()

print(dividend_yield_freq)
print(cash_dividend_freq)
print(cash_dividend_m1_freq)
print(cash_dividend_m2_freq)
print(proportional_dividend_freq)
print(dividend_yield_forward)
print(cash_dividend_forward)
print(cash_dividend_m1_forward)
print(cash_dividend_m2_forward)
print(proportional_dividend_forward)


'''
# [3.9424289966357033, 4.21623893697899, 4.356583873411636, 4.451563121902687, 4.4755012591324395, 4.487500311199823, 4.497915066989274]
# [3.9821585316279577, 3.973347544683029, 3.9690642989938034, 3.9661751823207125, 3.9654580005882045, 3.963575144635045, 3.964785179264228]
# [3.9423121816462143, 3.9436543081391044, 3.944322133738035, 3.9447661505682543, 3.9448770055844773, 3.9449324106370645, 3.944980416240857]
# [98.74000682693998, 99.23931153890233, 99.48825990282813, 99.6542823804078, 99.6958149169101, 99.71658671090817, 99.73459219479625]
# [98.74163909389061, 98.74371627899268, 98.74474141988416, 98.74543134184538, 98.74560311854385, 98.7452962614366, 98.74576387910702]
# [98.73998892467283, 98.742482358734, 98.74372284607735, 98.74454754618947, 98.74475343576603, 98.74485633781202, 98.74494549655148]
# '''