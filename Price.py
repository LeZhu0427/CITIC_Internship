import math
import numpy as np
from Option import Option
from PricingModel import PricingModel, ModelType
from MarketData import MarketData, DividendType


def Price(option: Option, market: MarketData, model: PricingModel, print_details: bool = True):
    if model.model_type() == ModelType.MonteCarlo:
        result = option.PriceByPath(model.generate_ST(S0=market.spot, vol=market.vol, r=market.r / 360,
                                                    T=option.T, t=option.t, d=market.d, d_model1=market.d_model1,
                                                    d_model2=market.d_model2, q=market.q, delta=market.delta,
                                                    frequency=market.frequency))
    elif model.model_type() == ModelType.Analytic:
        result = option.PriceByBS(market)
    else:
        raise NotImplementedError
    if print_details:
        print(option.option_type(), model.model_type(), market.div_type, result)
    return result

