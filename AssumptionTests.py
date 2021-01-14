import pandas as pd
import numpy as np
import statistics
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as stats

file_name = '500_FUTURES'
#file_name = '300_FUTURES'
#file_name = '50_FUTURES'

raw_data = pd.read_excel('./data/'+file_name+'.xls')
df = raw_data.drop_duplicates(subset=['TRADE_DT', 'UNDERLYING_CLOSE_PRICE'], keep='first').reset_index(drop=True)
df['log_return'] = np.log(df.UNDERLYING_CLOSE_PRICE) - np.log(df.UNDERLYING_CLOSE_PRICE.shift(-1))

# vol for n future days
def historical_val(series, window):
    result = [np.nan]*window
    for i in range(window, len(series)):
        result.append(statistics.stdev(series[i-window:i]))
    return result

df['vol_21d'] = historical_val(df['log_return'],21)
df['vol_63d'] = historical_val(df['log_return'],63)
df['vol_126d'] = historical_val(df['log_return'],126)
df['vol_189d'] = historical_val(df['log_return'],189)

# corrolation matrix
corr_matrix = df[['vol_21d', 'vol_63d', 'vol_126d', 'vol_189d']].dropna().corr()
print('corr_matrix')
print(corr_matrix)

# QQ Plot
mu = df['log_return'].mean()
sigma = statistics.stdev(df['log_return'].dropna())
sm.qqplot(df['log_return'].dropna(), stats.norm, loc=mu, scale=sigma, line ='45')   #stats.norm(loc=mu, scale=sigma)
plt.savefig("./results/QQPlot"+file_name+".png")
plt.show()

# KS Test
KS = stats.kstest(df['log_return'].dropna(), 'norm')
print()
print('KS Test')
print('D value: ', KS[0])
print('P value: ', KS[1])

# Skewness
skew = stats.skew(df['log_return'].dropna())
print('Skewness: ', skew)
plt.hist(df['log_return'], bins=30)
plt.savefig("./results/histogram"+file_name+".png")
plt.show()

# Kurtosis
kurtosis = stats.kurtosis(df['log_return'].dropna())
print('Kurtosis: ', kurtosis)

# Stationary
# unit root
# DF test
# demean time series is white noise
# Box-Ljung test
# ACF

#pd.set_option('display.max_columns', None)
#print(df)
#print(df.info())


'''
           vol_21d   vol_63d  vol_126d  vol_189d
vol_21d   1.000000  0.507497  0.220444 -0.019787
vol_63d   0.507497  1.000000  0.541787  0.314606
vol_126d  0.220444  0.541787  1.000000  0.501899
vol_189d -0.019787  0.314606  0.501899  1.000000

KS Test
D value:  0.4812233578877667
P value:  3.007294025524599e-156
Skewness:  -0.8028432972096649
Kurtosis:  3.8544765412961937
'''