import requests
import json
import time
import os
from dotenv import load_dotenv
import yfinance as yf


load_dotenv()

data = {}

data['potential_calls'] = []

api_key = os.getenv("api_key")

low_price = 5
high_price = 15
market_cap = 2000000000
volume = 500000
option_expiration = "2021-02-19"


failed_symbols = []
symbols = ['ETRN']

counter = len(symbols)
print("There are", len(symbols), "tickers available.")

for symbol in symbols:
    counter = counter-1
    print(len(symbols) - counter, "of", len(symbols))
    try:

        ticker = yf.Ticker(symbol)

        day_200 = ticker.history(period="6mo")
        print(type(day_200))

        previous_close = ticker.get_info()['previousClose']

        current_puts = ticker.option_chain().puts
        puts_strike_bid = current_puts.filter(items=['strike', 'bid'])
        greater_than_prev_close = puts_strike_bid[puts_strike_bid['strike']
                                                  > previous_close].iloc[0]

        next_strike = greater_than_prev_close[0]
        next_bid = greater_than_prev_close[1]
        max_value = next_strike + next_bid
        initial_investment = previous_close
        max_profit = (max_value/initial_investment) - 1
        min_profit = next_bid / previous_close

        print(next_strike)
        print(next_bid)
        print(min_profit)

        if min_profit > 0.08 and previous_close < high_price:
            data['potential_calls'].append({
                "ticker": symbol,
                "close": previous_close,
                "strike": next_strike,
                "premium": next_bid,
                "max_profit": "{:.2%}".format(max_profit),
                "min_profit": "{:.2%}".format(min_profit)
            })

        time.sleep(5)
    except Exception as e:
        failed_symbols.append(symbol)


# print('{} symbols were added'.format(len(data['potential_calls'])))
# print('{} symbols did not have options.'.format(len(failed_symbols)))
# print(failed_symbols)
