import yfinance as yf
import requests
import json
import time
import os

from dotenv import load_dotenv
load_dotenv()

data = {}

data['potential'] = []

api_key = os.getenv("api_key")

low_price = 5
high_price = 15
market_cap = 2000000000
volume = 500000
counter = 0
failed_symbols = []
symbols = []

screener = requests.get(
    f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={market_cap}&exchange=nasdaq&volumeMoreThan{volume}priceMoreThan={low_price}&priceLowerThan={high_price}&apikey={api_key}').json()
for item in screener:
    symbols.append(item['symbol'])

print("There are", len(symbols), "tickers available.")

for symbol in symbols:
    try:

        ticker = yf.Ticker(symbol)
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

        if min_profit > 0.08:
            data['potential'].append({
                "ticker": symbol,
                "close": previous_close,
                "strike": next_strike,
                "premium": next_bid,
                "max_profit": "{:.2%}".format(max_profit),
                "min_profit": "{:.2%}".format(min_profit)
            })

        counter = counter+1
        print(counter, "of", len(symbols))
        time.sleep(5)
    except Exception as e:
        failed_symbols.append(symbol)


print('{} symbols were added'.format(len(data['potential'])))
print('{} symbols failed.'.format(len(failed_symbols)))

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
