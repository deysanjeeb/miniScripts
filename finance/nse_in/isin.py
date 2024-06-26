import yfinance as yf
import pandas as pd
from pprint import pprint

def search_stock_by_isin(isin):
    try:
        # Search for the stock using the ISIN
        stock = yf.Ticker(isin)
        
        # Get the stock info
        info = stock.info
        
        # Check if we got valid data
        if 'longName' in info:
            return {
                'name': info['longName'],
                'symbol': info['symbol'],
                'exchange': info['exchange']
            }
        else:
            return None
    except Exception as e:
        print(isin)
        print(f"An error occurred: {e}")
        return None

# Example usage

df = pd.read_csv('pg8to12.csv')
print(df['Tables ISIN'])
stock_results= {}
for isin in df['Tables ISIN']:
    result = search_stock_by_isin(isin)

    if result:
        print(f"Stock Name: {result['name']}")
        print(f"Symbol: {result['symbol']}")
        print(f"Exchange: {result['exchange']}")
        stock_results[isin] = result
    else:
        print("Stock not found or there was an error in the search.")
        stock_results[isin] = None

pprint(stock_results)