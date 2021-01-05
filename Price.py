import math
import numpy as np
from Option import Option
from PricingModel import PricingModel, ModelType
from MarketData import MarketData, DividendType


def Price(option: Option, market: MarketData, model: PricingModel, print_details: bool = True):
    if model.model_type() == ModelType.MonteCarlo:
        result = option.PriceByPath(model.generate_ST(S0=market.spot, vol=market.vol, r=market.r / 360,
                                                    T=option.T, t=option.t, d=market.d, q=market.q,
                                                    delta=market.delta, frequency=market.frequency))
    elif model.model_type() == ModelType.Analytic:
        result = option.PriceByBS(market)
    else:
        raise NotImplementedError
    if print_details:
        print(option.option_type(), model.model_type(), market.div_type, result)
    return result


'''def Price(option_name, parameters, model):
    optionA = option_name.create(parameters)
    if parameters['type'] == 'dividend yield':
        return optionA.PriceByPath(model(parameters).generate_path_dividend_yield())
    elif parameters['type'] == 'discrete cash dividend':
        return optionA.PriceByPath(model(parameters).generate_path_discrete_cash_dividend())
    # discrete proportional dividend
    else:
        return optionA.PriceByPath(model(parameters).generate_path_discrete_proportional_dividend())'''
