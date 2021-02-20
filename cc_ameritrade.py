import requests
import json
import time
import traceback
import os
from dotenv import load_dotenv
import yfinance as yf


load_dotenv()

data = {}

data['potential_calls'] = []

api_key = os.getenv("api_key")
td_consumer_key = os.getenv('td_consumer_key')

low_price = 5
high_price = 20
market_cap = 2000000000
volume = 500000
expiration_length = 'monthly'
option_expiration = '2021-03-19'

min_profit_pct = 0.08

if expiration_length == "weekly":
    min_profit_pct = 0.03


failed_symbols = []
symbols = []

screener = requests.get(
    f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={market_cap}&isActivelyTrading=true&exchange=nasdaq,nyse&volumeMoreThan={volume}&priceMoreThan={low_price}&priceLowerThan={high_price}&apikey={api_key}').json()
for item in screener:
    symbols.append(item['symbol'])


counter = len(symbols)
print("There are", len(symbols), "tickers available.")

for symbol in symbols:
    counter = counter-1
    print(len(symbols) - counter, "of", len(symbols))
    try:

        ticker = yf.Ticker(symbol)

        try:
            day_200 = ticker.history(period="200d")["Close"].rolling(
                200, min_periods=1).mean()
            day_50 = ticker.history(period="50d")["Close"].rolling(
                50, min_periods=1).mean()
            day_18 = ticker.history(period="18d")["Close"].rolling(
                18, min_periods=1).mean()
        except Exception as e:
            pass

        ticker_info = ticker.get_info()

        previous_close = ticker_info['previousClose']

        current_puts = ticker.option_chain().puts

        base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}'
        endpoint = base_url.format(stock_ticker=symbol,
                                   contractType='Call',
                                   date=option_expiration)

        page = requests.get(url=endpoint,
                            params={'apikey': td_consumer_key})
        content = json.loads(page.content)
        put_map = content['putExpDateMap']

        target_exp_date = list(put_map.keys())[0]

        all_puts = put_map[target_exp_date]

        strike_price_list = list(all_puts.keys())
        strike_price_list_float = []

        for strike in strike_price_list:
            strike_price_list_float.append(float(strike))

        puts_greater_than_close = sorted(
            i for i in strike_price_list_float if i >= previous_close)
        next_call_value = puts_greater_than_close[0]

        next_call_object = all_puts[str(next_call_value)][0]

        final_strike = next_call_value
        final_bid = next_call_object['bid']

        max_value = final_strike + final_bid
        initial_investment = previous_close
        max_profit = (max_value/initial_investment) - 1
        min_profit = final_bid / previous_close

        if min_profit > min_profit_pct and previous_close < high_price and day_18.mean() > day_50.mean() > day_200.mean():
            data['potential_calls'].append({
                "ticker": symbol,
                "close": previous_close,
                "strike": final_strike,
                "premium": final_bid,
                "max_profit": "{:.2%}".format(max_profit),
                "min_profit": "{:.2%}".format(min_profit)
            })

        time.sleep(5)
    except Exception as e:
        pass


print('{} symbols were added'.format(len(data['potential_calls'])))


with open('TD_CC.json', 'w') as outfile:
    json.dump(data, outfile)
