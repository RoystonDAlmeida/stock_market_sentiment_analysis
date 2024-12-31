import yfinance as yf
import pandas as pd
from datetime import datetime

def is_trading_day(date):
    """
    Check if the given date is a trading day.

    @Args:
    - date: datetime object

    @Returns:
    - bool: True if it's a trading day, False otherwise.
    """
    # Check if the date is a weekday (Monday=0, Sunday=6)
    if date.weekday() >= 5:  # Saturday or Sunday
        return False

    # Add more holiday checks if needed (e.g., New Year's Day, Independence Day)
    holidays = [
        '2024-01-01',  # New Year's Day
        '2024-07-04',  # Independence Day
        '2024-12-25',  # Christmas Day
        # Add more holidays as needed
    ]

    # Convert holidays to datetime objects for comparison
    holidays = pd.to_datetime(holidays)

    return date not in holidays


def fetch_current_stock_price(ticker):
    """
    Fetches the current stock price for the given ticker symbol if today is a trading day.

    @Args:
    - ticker: Stock ticker symbol (e.g., 'AAPL')

    @Returns:
    - current_price: float or None, current stock price or None if not available.
    """
    today = datetime.now().date()

    if not is_trading_day(today):
        print("Today is not a trading day. Skipping stock price fetch.")
        return None

    # Fetch stock data using yfinance
    stock = yf.Ticker(ticker)

    # Get today's stock data
    stock_info = stock.history(period="1d")

    if len(stock_info) == 0:
        print("No data available for this ticker.")
        return None

    # Get current price from today's data
    current_price = stock_info['Close'].iloc[-1]

    return current_price