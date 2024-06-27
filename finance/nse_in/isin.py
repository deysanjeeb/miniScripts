import yfinance as yf
import pandas as pd
from pprint import pprint
import csv 
from datetime import datetime as dt
from datetime import date, timedelta


def search_stock_by_isin(isin, date):
    try:
        # Search for the stock using the ISIN
        stock = yf.Ticker(isin)
        dat = dt.strptime(date, '%Y-%m-%d')
        end = dat + timedelta(days=1)
        print(dat)
        # Get the stock info
        info = stock.info
        # pprint(info)
        try:
            prices = yf.download(info['symbol'], start=dat, end=end)

        
            if 'longName' in info:
                return {
                    'name': info['longName'],
                    'symbol': info['symbol'],
                    'exchange': info['exchange'],
                    'Open': prices['Open'].iloc[0],
                    'High': prices['High'].iloc[0],
                    'Low': prices['Low'].iloc[0],
                    'Close': prices['Close'].iloc[0],
                    'currentMarketPrice': info['regularMarketOpen']
                }
            else:
                return None
        except:
            if 'longName' in info:
                return {
                        'name': info['longName'],
                        'symbol': info['symbol'],
                        'exchange': info['exchange'],
                        'Open': None,
                        'High': None,
                        'Low': None,
                        'Close': None,
                        'currentMarketPrice': info['regularMarketOpen']
                    }
            else:
                return None

    except Exception as e:
        print(isin)
        print(f"An error occurred: {e}")
        return None


# Example usage
filename = 'KPK158'
df = pd.read_csv(f'{filename}.csv')
print(df['ISINNO'])
date = '2018-01-31'

stock_results= {}
for isin in df['ISINNO']:
    try:
        result = search_stock_by_isin(isin, date)
        
    except:
        stock = yf.Ticker(isin)
        info = stock.info
        result = {
            'name': info['longName'],
            'symbol': info['symbol'],
            'exchange': info['exchange'],
            'Open': None,
            'High': None,
            'Low': None,
            'Close': None,
            'currentMarketPrice': info['regularMarketOpen']
        }

    if result:
        print(f"Stock Name: {result['name']}")
        print(f"Symbol: {result['symbol']}")
        print(f"Exchange: {result['exchange']}")
        print(f"Open: {result['Open']}")
        print(f"current_price {result['currentMarketPrice']}")
        stock_results[isin] = result

    else:
        print("Stock not found or there was an error in the search.")
        stock_results[isin] = None

pprint(stock_results)
with open(f'{filename}_stock_results_{date}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['ISIN', 'Stock Name', 'Symbol', 'Exchange', 'Open', 'High', 'Low', 'Close', 'currentMarketPrice'])
    
    # Write the data
    for isin, info in stock_results.items():
        if info:  # If there is a result for the ISIN
            writer.writerow([isin, info['name'], info['symbol'], info['exchange'], info['Open'], info['High'], info['Low'], info['Close'], info['currentMarketPrice']])
        else:  # If the search was unsuccessful or there was an error
            writer.writerow([isin, 'Not Found', 'Not Found', 'Not Found'])