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
    
    # Simulating past failed trades (random losses for testing)
    failed_trades = [
        {"entry_price": daily_prices[i+5], "exit_price": daily_prices[i], "date": list(daily_data["Time Series (Daily)"].keys())[i]}
        for i in range(5, 10) if daily_prices[i] < daily_prices[i+5]
    ]

    print(f"\n📊 **Trade Simulation & Recovery Plan for {company_name} ({SYMBOL})**\n")
    
    if not failed_trades:
        print("✅ No major past trade failures detected.")
        exit()

    print("❌ **Past Failed Trades:**")
    for trade in failed_trades:
        loss = trade["entry_price"] - trade["exit_price"]
        print(f"📅 Date: {trade['date']} | Entry: ${trade['entry_price']:.2f} | Exit: ${trade['exit_price']:.2f} | Loss: ${loss:.2f}")

    # AI Strategy Simulation: Monte Carlo (randomized backtest)
    num_simulations = 1000
    stop_loss_options = [0.02, 0.05, 0.1]  # 2%, 5%, 10% stop-loss levels
    success_rates = {}

    for stop_loss in stop_loss_options:
        wins = 0
        for _ in range(num_simulations):
            simulated_exit = random.choice(daily_prices[:10]) * (1 - stop_loss)
            if simulated_exit > failed_trades[0]["exit_price"]:
                wins += 1
        success_rates[f"{int(stop_loss*100)}% Stop-Loss"] = (wins / num_simulations) * 100

    print("\n🔍 **AI-Powered Recovery Analysis:**")
    for sl, success in success_rates.items():
        print(f"✅ {sl}: {success:.2f}% success rate in backtests.")

    best_strategy = max(success_rates, key=success_rates.get)
    print(f"\n💡 **Suggested Alternative Strategy:** {best_strategy} for better risk management.")

except KeyError:
    print("⚠️ Error: Unable to fetch stock data. Check API key or company name.")
