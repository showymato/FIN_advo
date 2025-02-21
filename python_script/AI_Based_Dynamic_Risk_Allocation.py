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
    "Nvidia": "NVDA",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD"
}

# Get the stock symbol
SYMBOL = company_symbols.get(company_name)
if not SYMBOL:
    print("⚠️ Error: Company not found. Try using a stock symbol.")
    exit()

# Replace with your Alpha Vantage API Key
API_KEY = '0H56TMW7D97Z9PQO'

# API URL
DAILY_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&outputsize=compact&apikey={API_KEY}'

# Fetch Daily Data
daily_response = requests.get(DAILY_URL)
daily_data = daily_response.json()

# Extract closing prices from daily data
try:
    daily_prices = [float(value["4. close"]) for key, value in daily_data["Time Series (Daily)"].items()]
    volatility = np.std(daily_prices[:10]) / np.mean(daily_prices[:10]) * 100  # 10-day volatility (%)
    price_trend = daily_prices[0] - daily_prices[5]  # Price difference in 5 days

    # AI-Based Risk Signal
    if volatility > 20 or price_trend < 0:
        risk_signal = "High-Risk 🚨"
        action = "Reduce Allocation ⬇️"
    elif price_trend > 0:
        risk_signal = "Bullish ✅"
        action = "Increase Position ⬆️"
    else:
        risk_signal = "Neutral 📊"
        action = "Hold 🔄"

    # Hedging Strategies
    if risk_signal == "High-Risk 🚨":
        hedge_suggestion = "🔹 Suggested Hedge: Use options/futures or shift to stable assets."
        if SYMBOL in ["BTC-USD", "ETH-USD"]:
            hedge_suggestion += " Consider moving funds to stablecoins (USDT, USDC)."
    else:
        hedge_suggestion = "🔹 No immediate hedging required."

    # Output AI-based recommendations
    print(f"\n📊 **Dynamic Risk Allocation Report for {company_name} ({SYMBOL})**")
    print(f"✅ Market Volatility: {volatility:.2f}%")
    print(f"📈 Price Trend (5 Days): {'Up 📈' if price_trend > 0 else 'Down 📉'} (${price_trend:.2f})")
    print(f"⚠️ AI Risk Signal: {risk_signal}")
    print(f"💡 Suggested Action: {action}")
    print(hedge_suggestion)

except KeyError:
    print("⚠️ Error: Unable to fetch stock data. Check API key or company name.")
