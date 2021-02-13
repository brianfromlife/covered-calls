# Covered Calls

Before running this script please make sure you have python 3.8+ installed.

If you are not familiar with code, I would highly recommend installing `Visual Studio Code` to perform the steps below.

This script will screen FMP for stocks with a $2B+ market cap, volume more than 500,000, a minimum price of $5 and a maximum price of $15. Then it will check the Yahoo Finance Options Chain for a certain expiration date and grab the nearest strike price of the previous close.

Note: You can change the above criteria by editing lines 17-21 in `main.py`.

1. generate a free API Key from `https://financialmodelingprep.com/`.
2. Create a file called `.env` in this folder.
3. Add `api_key=XXX` to the `.env` file. Replace `XXX` with the API Key from FMP.
4. In the terminal, run `python main.py`. The terminal should begin to show progress.
5. After the script is finished a file named `covered_calls.json` will appear in the folder with the list of potential covered calls with a minimum profit of 8% or more.
