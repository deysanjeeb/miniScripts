import pandas as pd
from nsepy import get_history
from datetime import date
import csv
from difflib import SequenceMatcher


def match_ratio(s1, s2):
    # Use SequenceMatcher to compare the two strings
    return SequenceMatcher(None, s1, s2).ratio()

# Verify a ticker by fetching recent data
def verify_ticker(ticker):
    try:
        data = get_history(symbol=ticker, start=date(2023,1,1), end=date.today())
        if len(data) > 0:
            return f"Ticker {ticker} is valid. Last trading day: {data.index[-1]}"
        else:
            return f"No data found for ticker {ticker}"
    except Exception as e:
        return f"Error verifying ticker {ticker}: {str(e)}"
    
nse_list = pd.read_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv')
print(nse_list)
def find_nse_ticker(company_name):
    try:
        # Load the list of NSE symbols
        
        # Convert company name to lowercase for case-insensitive search
        company_name_lower = company_name.lower()
        
        # # Search for the company in the list
        # matches = nse_list[nse_list['NAME OF COMPANY'].str.lower().str.contains(company_name_lower)]
        
        mask = nse_list['NAME OF COMPANY'].apply(lambda x: match_ratio(x.lower(), company_name_lower) > 0.6)

        # Apply the mask to the DataFrame to get matches
        matches = nse_list[mask]

        if len(matches) == 0:
            return "No matches found"
        elif len(matches) == 1:
            return matches.iloc[0]['SYMBOL']
        else:
            return matches[['SYMBOL', 'NAME OF COMPANY']].to_dict('records')

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
company_names = []
col = pd.read_csv('gool.csv', header=None)
col = col[0].tolist()
for name in col:
    name = name.split('- NSE')[0]
    company_names.append(name)

print(company_names)
tickers=[]
for name in company_names:
    result = find_nse_ticker(name)
    print(f"Company: {name}")
    print(f"Result: {result}")
    tickers.append(result)
    print()

with open('tickers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for ticker in tickers:
        writer.writerow([ticker])  # Write each ticker as a row

print("Tickers have been written to tickers.csv")
