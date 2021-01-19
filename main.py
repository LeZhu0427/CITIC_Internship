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
#frequency = [1]
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
plt.plot(frequency, dividend_yield_freq, marker = '.',label='dividend_yield')
plt.plot(frequency, cash_dividend_freq, label='cash_dividend')
#plt.plot(frequency, cash_dividend_m1_freq, label='cash_dividend_m1')
#plt.plot(frequency, cash_dividend_m2_freq, label='cash_dividend_m2')
plt.plot(frequency, proportional_dividend_freq, marker='x', label='proportional_dividend')
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
plt.plot(frequency, dividend_yield_forward, marker='.',label='dividend_yield_forward')
plt.plot(frequency, cash_dividend_forward, label='cash_dividend_forward')
#plt.plot(frequency, cash_dividend_m1_forward, label='cash_dividend_m1_forward')
#plt.plot(frequency, cash_dividend_m2_forward, label='cash_dividend_m2_forward')
plt.plot(frequency, proportional_dividend_forward, marker='x', label='proportional_dividend_forward')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('forward price')
plt.savefig("./results/frequency-forward.png")
plt.show()

plt.plot(frequency, cash_dividend_m1_freq, marker='.', label='cash_dividend_m1')
plt.plot(frequency, cash_dividend_freq, label='cash_dividend')
plt.plot(frequency, cash_dividend_m2_freq, marker='x', label='cash_dividend_m2')
plt.legend()
plt.xlabel('dividend frequency')
plt.ylabel('European call price (cash dividend)')
plt.savefig("./results/frequency-price_cash.png")
plt.show()

plt.plot(frequency, cash_dividend_m1_forward, marker='.', label='cash_dividend_m1_forward')
plt.plot(frequency, cash_dividend_forward, label='cash_dividend_forward')
plt.plot(frequency, cash_dividend_m2_forward, marker='x', label='cash_dividend_m2_forward')
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
[3.930826667489031, 3.932123020372515, 3.9327680332970716, 3.933196878734849, 3.933303944392314, 3.9333966883499922, 3.933403820668521]
[3.9704380965799007, 3.9617684523070076, 3.957413331777685, 3.954529673033689, 3.953810646770969, 3.953186829772341, 3.9531391103793103]
[3.9307098507299245, 3.9320064760746254, 3.9326516246286016, 3.9330805602553776, 3.9331876484264487, 3.9332804118977394, 3.9332875457154923]
[3.9704247938951034, 3.9716221324702423, 3.972217885108573, 3.9726139810035965, 3.9727128707496293, 3.9727985323333836, 3.972805120012958]
[3.9307098507299156, 3.9320064760746294, 3.932651624628612, 3.9330805602554078, 3.9331876484265176, 3.933280411897462, 3.9332875457158485]
[98.97701257141928, 98.97951199288647, 98.98075545891159, 98.98158213927947, 98.98178852323433, 98.98196729691526, 98.98198104518829]
[98.97676717304562, 98.9793997003598, 98.98066349559801, 98.98149753277555, 98.98171204098477, 98.98189571144852, 98.98191021416723]
[98.97699950131454, 98.97949892049417, 98.98074238544137, 98.98156906511996, 98.98177544890655, 98.98195422244336, 98.98196797070082]
[98.9767393948825, 98.97923946432779, 98.98048325278322, 98.98131014753712, 98.98151658501838, 98.98169540506365, 98.98170915690007]
[98.97699950131457, 98.97949892049415, 98.98074238544135, 98.98156906512001, 98.98177544890667, 98.98195422244285, 98.98196797070153] '''