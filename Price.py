def Price(option_name, parameters, model):
    optionA = option_name(parameters)
    if parameters['type']=='dividend yield':
        return optionA.PriceByPath(model(parameters).generate_path_dividend_yield())
    elif parameters['type']=='discrete cash dividend':
        return optionA.PriceByPath(model(parameters).generate_path_discrete_cash_dividend())
    # discrete proportional dividend
    else:
        return optionA.PriceByPath(model(parameters).generate_path_discrete_proportional_dividend())
