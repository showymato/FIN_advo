import requests
import json
import numpy as np
import random

# User input: Company Name
company_name = input("Enter the company name (e.g., Apple, Tesla, IBM): ").strip().title()

# Mapping common company names to stock symbols (expandable)
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
    
    print(f"\n📊 **AI-Powered Loss Recovery Plan for {company_name} ({SYMBOL})**\n")

    # **Step 1: Cost-Averaging Strategy**
    print("📌 **Cost-Averaging Strategy:**")
    if daily_prices[0] < np.mean(daily_prices[:10]):  
        suggested_entry = daily_prices[0] * 0.98  # Suggest re-entry at 2% lower
        print(f"✅ Stock dropped. Consider gradual re-entry at: **${suggested_entry:.2f}** per share.")
    else:
        print("✅ Stock is stable. Avoid aggressive averaging.")

    # **Step 2: Portfolio Diversification**
    print("\n📌 **Portfolio Diversification Suggestions:**")
    safe_assets = ["Gold ETF", "Treasury Bonds", "Dividend Stocks", "S&P 500 Index"]
    suggested_asset = random.choice(safe_assets)
    print(f"✅ AI suggests adding **{suggested_asset}** for risk balance.")

    # **Step 3: AI-Based Risk Assessment**
    volatility = np.std(daily_prices[:10]) / np.mean(daily_prices[:10]) * 100
    print("\n📌 **AI-Based Risk Assessment:**")
    
    if volatility > 20:
        risk_level = "🔴 High Risk (Consider hedging)"
    elif volatility > 10:
        risk_level = "🟡 Moderate Risk (Set tighter stop-loss)"
    else:
        risk_level = "🟢 Low Risk (Safe to proceed with caution)"
    
    print(f"✅ AI Risk Rating for Next Trade: **{risk_level}**")

except KeyError:
    print("⚠️ Error: Unable to fetch stock data. Check API key or company name.")
