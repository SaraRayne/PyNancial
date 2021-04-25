import os
import requests

import numpy as np
import pandas as pd

from flask import redirect, render_template, request, session

KEY = os.environ.get("API_KEY")

# Used for reference: https://codingandfun.com/analyse-industry-stocks-python/
def query(cap, sector, exchange):

    """ RETRIEVE STOCKS THAT FIT CRITERIA (30 Stock limit) """

    market_cap = cap
    sector = sector
    exchange = exchange
    # List containing stocks that fit criteria
    symbols = []

    stock_results = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={market_cap}&betaMoreThan=0&volumeMoreThan=10000&sector={sector}&exchange={exchange}&dividendMoreThan=0&limit=30&apikey={KEY}').json()

    for stock in stock_results:
        symbols.append(stock['symbol'])

    # If no stocks were returned, exit
    if not symbols:
        return False

    """ COMPUTE PRICE TO EARNINGS RATIO """
    # Keep only that have low price to earnings (lower than market average)

    metrics = {}
    for company in symbols:
        try:
            # Get info on company
            company_data = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey={KEY}').json()
            # Get Income Statement for company
            IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&apikey={KEY}').json()

            # Get Earnings Per Share
            eps_diluted = [IS[0]['epsdiluted'], IS[1]['epsdiluted'], IS[2]['epsdiluted'], IS[3]['epsdiluted'], IS[4]['epsdiluted']]
            eps_diluted = np.array(eps_diluted).sum()

            # Get Price
            price = company_data[0]['price']

            # Put retrieved info into dictionary
            metrics[company] = {}
            # Price to earnings ratio
            metrics[company]['pe'] = price / eps_diluted

        except:
            pass

    # Create Pandas Dataframe
    all_companies = pd.DataFrame.from_dict(metrics,orient='index')
    # Find median price to earnings ratio for industry
    industry_median = all_companies['pe'].median()

    # Filter by companies w/ PE less than industry median
    all_companies = all_companies[all_companies.pe < industry_median]

    # List for all stocks w/ PE less than industry median
    value_stocks = all_companies.index.tolist()

    """ RETRIEVE DISCOUNTED CASH FLOW VALUATION """

    valuation = {}
    for company in value_stocks:
        try:
            DCF = requests.get(f'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{company}?apikey={KEY}').json()

            # Put retrieved info into dictionary
            valuation[company] = {}
            # DCF for stock
            valuation[company]['dcf'] = DCF[0]['dcf']
            # Latest price for stock
            valuation[company]['price'] = DCF[0]['Stock Price']

        except:
            pass

    """ COMPARE CURRENT PRICE TO PRICE FOUND IN VALUATION """

    for company in valuation:
        try:
            # Checks if the current price is higher than or equal to estimated value (as long as difference is more than $1)
            if valuation[company]['price'] >= ((valuation[company]['dcf']) - 1):
                # If price is higher or equal, stock is removed from list of value stocks
                value_stocks.remove(company)
        except(KeyError, TypeError, ValueError):
            pass

    data = []
    for stock in value_stocks:
        try:
            # Make list with all stock info needed to create an easier-to-sort dataframe
            data.append([stock, "{:.2f}".format(valuation[stock]["price"]), "{:.2f}".format(valuation[stock]["dcf"]), "{:.2f}".format((valuation[stock]["dcf"]) - (valuation[stock]["price"]))])

        except(KeyError,TypeError, ValueError):
            pass

    return(data)

""" Function for Daily Top Ten auto-search """
def top():

    # List containing stocks that fit criteria
    symbols = []

    stock_results = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=300000000&betaMoreThan=0&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=60&apikey={KEY}').json()

    for stock in stock_results:
        symbols.append(stock['symbol'])

    # If no stocks were returned, exit
    if not symbols:
        return False

    """ COMPUTE PRICE TO EARNINGS RATIO """
    # Keep only that have low price to earnings (lower than market average)

    metrics = {}
    for company in symbols:
        try:
            # Get info on company
            company_data = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey={KEY}').json()

            # Get Income Statement for company
            IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&apikey={KEY}').json()

            # Get Earnings Per Share
            eps_diluted = [IS[0]['epsdiluted'], IS[1]['epsdiluted'], IS[2]['epsdiluted'], IS[3]['epsdiluted'], IS[4]['epsdiluted']]
            eps_diluted = np.array(eps_diluted).sum()

            # Get Price
            price = company_data[0]['price']

            # Put retrieved info into dictionary
            metrics[company] = {}
            # Price to earnings ratio
            metrics[company]['pe'] = price / eps_diluted

        except:
            pass

    # Create Pandas Dataframe
    all_companies = pd.DataFrame.from_dict(metrics,orient='index')
    # Find median price to earnings ratio for industry
    industry_median = all_companies['pe'].median()

    # Filter by companies w/ PE less than industry median
    all_companies = all_companies[all_companies.pe < industry_median]

    # List for all stocks w/ PE less than industry median
    value_stocks = all_companies.index.tolist()

    """ RETRIEVE DISCOUNTED CASH FLOW VALUATION """

    valuation = {}
    for company in value_stocks:
        try:
            DCF = requests.get(f'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{company}?apikey={KEY}').json()

            # Put retrieved info into dictionary
            valuation[company] = {}
            # DCF for stock
            valuation[company]['dcf'] = DCF[0]['dcf']
            # Latest price for stock
            valuation[company]['price'] = DCF[0]['Stock Price']

        except:
            pass

    """ COMPARE CURRENT PRICE TO PRICE FOUND IN VALUATION """

    for company in valuation:
        try:
            # Checks if the current price is higher than or equal to estimated value (as long as difference is more than $1)
            if valuation[company]['price'] >= ((valuation[company]['dcf']) - 1):
                # If price is higher or equal, stock is removed from list of value stocks
                value_stocks.remove(company)
        except(KeyError, TypeError, ValueError):
            pass

    if not value_stocks:
        return False

    data = []
    for stock in value_stocks:
        try:
            # Make list with all stock info needed to create an easier-to-sort dataframe
            data.append([stock, "{:.2f}".format(valuation[stock]["price"]), "{:.2f}".format(valuation[stock]["dcf"]), "{:.2f}".format((valuation[stock]["dcf"]) - (valuation[stock]["price"]))])

        except(KeyError,TypeError, ValueError):
            pass

    return(data)

""" If user provides email address, this function will send them a full list of value stocks """
def full(cap, sector, exchange):

    market_cap = cap
    sector = sector
    exchange = exchange
    # List containing stocks that fit criteria
    symbols = []

    stock_results = requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={market_cap}&betaMoreThan=0&volumeMoreThan=10000&sector={sector}&exchange={exchange}&dividendMoreThan=0&limit=60&apikey={KEY}').json()

    for stock in stock_results:
        symbols.append(stock['symbol'])

    # If no stocks were returned, exit
    if not symbols:
        return False

    """ COMPUTE PRICE TO EARNINGS RATIO """
    # Keep only that have low price to earnings (lower than market average)

    metrics = {}
    for company in symbols:
        try:
            # Get info on company
            company_data = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{company}?apikey={KEY}').json()

            # Get Income Statement for company
            IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?period=quarter&apikey={KEY}').json()

            # Get Earnings Per Share
            eps_diluted = [IS[0]['epsdiluted'], IS[1]['epsdiluted'], IS[2]['epsdiluted'], IS[3]['epsdiluted'], IS[4]['epsdiluted']]
            eps_diluted = np.array(eps_diluted).sum()

            # Get Price
            price = company_data[0]['price']

            # Put retrieved info into dictionary
            metrics[company] = {}
            # Price to earnings ratio
            metrics[company]['pe'] = price / eps_diluted

        except:
            pass

    # Create Pandas Dataframe
    all_companies = pd.DataFrame.from_dict(metrics,orient='index')
    # Find median price to earnings ratio for industry
    industry_median = all_companies['pe'].median()

    # Filter by companies w/ PE less than industry median
    all_companies = all_companies[all_companies.pe < industry_median]

    # List for all stocks w/ PE less than industry median
    value_stocks = all_companies.index.tolist()

    """ RETRIEVE DISCOUNTED CASH FLOW VALUATION """

    valuation = {}
    for company in value_stocks:
        try:
            DCF = requests.get(f'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{company}?apikey={KEY}').json()

            # Put retrieved info into dictionary
            valuation[company] = {}
            # DCF for stock
            valuation[company]['dcf'] = DCF[0]['dcf']
            # Latest price for stock
            valuation[company]['price'] = DCF[0]['Stock Price']

        except:
            pass

    """ COMPARE CURRENT PRICE TO PRICE FOUND IN VALUATION """

    for company in valuation:
        try:
            # Checks if the current price is higher than or equal to estimated value (as long as difference is more than $1)
            if valuation[company]['price'] >= ((valuation[company]['dcf']) - 1):
                # If price is higher or equal, stock is removed from list of value stocks
                value_stocks.remove(company)
        except(KeyError, TypeError, ValueError):
            pass

    if not value_stocks:
        return False

    data = []
    for stock in value_stocks:
        try:
            # Make list with all stock info needed to create an easier-to-sort dataframe
            data.append([stock, "{:.2f}".format(valuation[stock]["price"]), "{:.2f}".format(valuation[stock]["dcf"]), "{:.2f}".format((valuation[stock]["dcf"]) - (valuation[stock]["price"]))])

        except(KeyError,TypeError, ValueError):
            pass

    return(data)