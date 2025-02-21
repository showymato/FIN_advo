import pandas as pd
import numpy as np
from alpha_vantage.cryptocurrencies import CryptoCurrencies

# Alpha Vantage API Key
api_key = "YOUR_ALPHA_VANTAGE_API_KEY"

# Initialize Alpha Vantage Client
cc = CryptoCurrencies(key=api_key, output_format='pandas')

def get_alpha_vantage_data(symbol="BTC", market="USD"):
    """
    Fetches historical crypto data (Bitcoin/USD) using Alpha Vantage API.
    """
    data, meta_data = cc.get_digital_currency_daily(symbol=symbol, market=market)

    # Renaming columns
    data = data[['1a. open (USD)', '2a. high (USD)', '3a. low (USD)', '4a. close (USD)', '5. volume']]
    data.columns = ['open', 'high', 'low', 'close', 'volume']

    # Convert index to datetime format
    data.index = pd.to_datetime(data.index)

    # Sort data by ascending date
    data = data.sort_index()

    return data

# Fetch Data
crypto_data = get_alpha_vantage_data()
print(crypto_data.head())
