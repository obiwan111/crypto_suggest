import ccxt
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init()

# Initialize the Binance exchange
exchange = ccxt.binance()

# Function to clear the console screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to fetch popular tokens
def fetch_popular_tokens(limit=5):
    try:
        markets = exchange.fetch_markets()
        symbols = [market['symbol'] for market in markets if 'spot' in market['type'].lower()][:limit]
        return symbols
    except Exception as e:
        print(f"Error fetching popular tokens: {e}")
        return []

# Function to fetch cryptocurrency data
def get_cryptocurrency_data(symbol, timeframe='1h', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return ohlcv
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to analyze the trend
def analyze_trend(data):
    closes = [candle[4] for candle in data]
    average_close = sum(closes) / len(closes)
    return "Bullish" if closes[-1] > average_close else "Bearish"

# Function to suggest actions for cryptocurrencies
def suggest_cryptocurrencies(symbols):
    buy_suggestions = []
    sell_suggestions = []
    
    for symbol in symbols:
        data = get_cryptocurrency_data(symbol)
        if data:
            trend = analyze_trend(data)
            latest_price = data[-1][4]  # Closing price of the latest candle
            
            # Construct a suggestion based on trend analysis
            suggestion_text = f"The current trend for {symbol} is {trend}. Latest Closing Price: {latest_price}."
            
            # Append the suggestion to the appropriate list
            if trend == "Bullish":
                buy_suggestions.append((suggestion_text, Fore.GREEN))
            else:
                sell_suggestions.append((suggestion_text, Fore.RED))
        else:
            print(f"Error fetching data for {symbol}")
    
    return buy_suggestions, sell_suggestions

# Function to print colored suggestions
def print_colored_suggestions(suggestions):
    for suggestion, color_code in suggestions:
        print(f"{color_code}{suggestion}{Style.RESET_ALL}")

# Main function
if __name__ == "__main__":
    try:
        while True:
            # Fetch popular tokens
            popular_tokens = fetch_popular_tokens(limit=5)
            
            # Get suggestions for each popular symbol
            buy_suggestions, sell_suggestions = suggest_cryptocurrencies(popular_tokens)
            
            # Print the colored suggestions
            print("\nBuy Suggestions:")
            print_colored_suggestions(buy_suggestions)
            
            print("\nSell Suggestions:")
            print_colored_suggestions(sell_suggestions)
            
            print("\nWaiting for the next update...\n")
            time.sleep(120)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        print("\nStopped.")
