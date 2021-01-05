import math
import numpy as np

def Price(option_name, parameters, model):
    option = option_name.create(parameters)
    if 'q' not in parameters.keys():
        parameters['q'] = np.zeros(parameters['T']-parameters['t'])
    if 'd' not in parameters.keys():
        parameters['d'] = np.zeros(parameters['T'] - parameters['t'])
    if 'delta' not in parameters.keys():
        parameters['delta'] = np.zeros(parameters['T'] - parameters['t'])
    return option.PriceByPath(model.generate_ST(S0=parameters['S0'], vol=parameters['vol'], r=parameters['r']/360,
                              T=parameters['T'], t=parameters['t'], d=parameters['d'], q=parameters['q'], delta=parameters['delta']))


'''def Price(option_name, parameters, model):
    optionA = option_name.create(parameters)
    if parameters['type'] == 'dividend yield':
        return optionA.PriceByPath(model(parameters).generate_path_dividend_yield())
    elif parameters['type'] == 'discrete cash dividend':
        return optionA.PriceByPath(model(parameters).generate_path_discrete_cash_dividend())
    # discrete proportional dividend
    else:
        return optionA.PriceByPath(model(parameters).generate_path_discrete_proportional_dividend())'''
