import requests
import json
import numpy as np

# User input: Company Name
company_name = input("Enter the company name (e.g., Apple, Tesla, IBM): ").strip().title()

# Mapping common company names to stock symbols (you can expand this list)
company_symbols = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "IBM": "IBM",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Meta": "META",
    "Nvidia": "NVDA"
}

# Get the stock symbol
SYMBOL = company_symbols.get(company_name)
if not SYMBOL:
    print("⚠️ Error: Company not found. Try using a stock symbol.")
    exit()

# Replace with your Alpha Vantage API Key
API_KEY = '0H56TMW7D97Z9PQO'

# API URLs
DAILY_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize=compact&apikey={API_KEY}'

# Fetch Daily Data
daily_response = requests.get(DAILY_URL)
daily_data = daily_response.json()

# Extract closing prices from daily data
try:
    daily_prices = [float(value["4. close"]) for key, value in daily_data["Time Series (Daily)"].items()]
    volatility = np.std(daily_prices[:10]) / np.mean(daily_prices[:10]) * 100  # 10-day volatility (%)

    # AI-based stop-loss strategy
    if volatility > 20:
        stop_loss = 0.02  # 2% stop-loss for high volatility
    elif volatility > 10:
        stop_loss = 0.05  # 5% for moderate volatility
    else:
        stop_loss = 0.07  # 7% stop-loss for stable assets

    # Implement Trailing Stop-Loss
    current_price = daily_prices[0]  # Latest closing price
    trailing_stop = current_price * (1 - stop_loss)

    # Output AI-based recommendations
    print(f"\n📊 **Automated Risk Management Report for {company_name} ({SYMBOL})**")
    print(f"✅ Market Volatility: {volatility:.2f}%")
    print(f"💡 Suggested Stop-Loss: {stop_loss * 100:.2f}%")
    print(f"🔹 Recommended Trailing Stop Price: ${trailing_stop:.2f}")

except KeyError:
    print("⚠️ Error: Unable to fetch stock data. Check API key or company name.")
