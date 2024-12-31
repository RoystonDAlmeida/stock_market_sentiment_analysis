import pandas as pd
from datetime import timedelta

def get_last_trading_day_price(combined_data):
    """
    Get the last trading day's closing price from combined_data.

    @Args:
    - combined_data: DataFrame containing stock data with 'Date' and 'Close' columns.

    @Returns:
    - last_trading_day_price: float, closing price of the last trading day.
    - last_trading_day_date: string, date of the last trading day in 'YYYY-MM-DD' format.
    """

    # Ensure 'Date' is in datetime format
    combined_data['Date'] = pd.to_datetime(combined_data['Date'])

    # Sort by date to ensure we have the latest data
    combined_data = combined_data.sort_values(by='Date')

    # Get the latest available date
    last_date = combined_data['Date'].iloc[-1]

    # Check if the last date is a weekday (Monday to Friday)
    if last_date.dayofweek < 5:  # 0=Monday, 1=Tuesday, ..., 6=Sunday
        # If it's a weekday, return its closing price
        last_trading_day_price = combined_data.loc[combined_data['Date'] == last_date, 'Close'].values[0]
        return last_trading_day_price, last_date.strftime('%Y-%m-%d')

    # If it's a weekend or holiday, find the previous trading day
    for i in range(1, 8):  # Check up to 7 days back
        previous_date = last_date - timedelta(days=i)
        if previous_date in combined_data['Date'].values:
            last_trading_day_price = combined_data.loc[combined_data['Date'] == previous_date, 'Close'].values[0]
            return last_trading_day_price, previous_date.strftime('%Y-%m-%d')

    return None, None  # In case no valid trading day is found