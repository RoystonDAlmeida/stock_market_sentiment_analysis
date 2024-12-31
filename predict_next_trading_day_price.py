import requests
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Accessing the API key and URL
api_key = os.getenv('EOD_API_TOKEN')
api_url = os.getenv('EOD_API_URL')


def fetch_news_sentiment(ticker, date):
    """
    Fetches news sentiment data for the given ticker symbol from EODHD API.

    @Args:
    - ticker: Stock ticker symbol (e.g., 'AAPL')
    - date: Date in 'YYYY-MM-DD' format for which to fetch sentiment data.

    @Returns:
    - latest_sentiment: dict containing average 'neg', 'neu', 'pos' sentiment scores.
    """

    url = f"{api_url}?s={ticker.upper()}&from={date}&to={date}&limit=100&api_token={api_key}&fmt=json"

    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        print(news_data)

        # Check if the news_data is empty
        if not news_data or not isinstance(news_data, list) or len(news_data) == 0:
            print(f"No news data available for {ticker} on {date}. Returning default values.")
            return {'neg': 0, 'neu': 0, 'pos': 0}  # Default values if no data is available

        # Initialize sums and counts for averaging
        total_neg = total_neu = total_pos = 0
        count = len(news_data)

        # Aggregate sentiment scores from all news items
        for item in news_data:
            sentiment = item.get('sentiment', {})
            total_neg += sentiment.get('neg', 0)
            total_neu += sentiment.get('neu', 0)
            total_pos += sentiment.get('pos', 0)

        # Calculate average sentiment scores
        return {
            'neg': total_neg / count,
            'neu': total_neu / count,
            'pos': total_pos / count
        }

    print(f"Failed to fetch news sentiment for {ticker} on {date}. Returning default values.")
    return {'neg': 0, 'neu': 0, 'pos': 0}  # Default values if fetching fails or no data is available

def predict_next_trading_day_price(combined_data, model, ticker, imputer, scaler):
    """
    Predicts the next trading day's stock price using the trained model and latest data.

    @Args:
    - combined_data: DataFrame containing stock and sentiment data up to previous trading day.
    - model: Trained RidgeCV model.
    - ticker: Stock ticker symbol to fetch new sentiment data.
    - imputer: Fitted SimpleImputer instance(same imputer used in training).
    - scaler: Fitted StandardScaler instance(same sclaer used in training).

    @Returns:
    - predicted_price: float, predicted stock price for the next trading day.
    """

    # Ensure combined_data is sorted by date and contains no NaN values
    combined_data = combined_data.dropna(subset=['Close', 'High', 'Low', 'Volume', 'neg', 'neu', 'pos'])

    # Fetch new sentiment data for today's date(US time zone)
    today_date = (pd.to_datetime("now").tz_localize('US/Eastern').strftime('%Y-%m-%d'))
    print("Today's Date in US:", today_date)
    latest_sentiment = fetch_news_sentiment(ticker, today_date)

    # Extract the last row (most recent trading day)
    latest_data = combined_data.iloc[-1].copy()

    # Prepare features for prediction using fetched sentiments
    daily_return = (latest_data['Close'] - combined_data['Close'].iloc[-2]) / combined_data['Close'].iloc[-2]

    # Calculate moving averages
    sma_5 = combined_data['Close'].rolling(window=5).mean().iloc[-1]
    sma_20 = combined_data['Close'].rolling(window=20).mean().iloc[-1]

    # Calculate RSI (14-day)
    delta = combined_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    # Calculate MACD
    ema_12 = combined_data['Close'].ewm(span=12, adjust=False).mean().iloc[-1]
    ema_26 = combined_data['Close'].ewm(span=26, adjust=False).mean().iloc[-1]
    macd = ema_12 - ema_26

    # Calculate ATR (14-day)
    high_low = combined_data['High'] - combined_data['Low']
    high_close = abs(combined_data['High'] - combined_data['Close'].shift())
    low_close = abs(combined_data['Low'] - combined_data['Close'].shift())


    tr = high_low.combine(high_close, max).combine(low_close, max)
    atr = tr.rolling(window=14).mean().iloc[-1]

    # Calculate average volume over a specified period
    avg_volume_5 = combined_data['Volume'].rolling(window=5).mean().iloc[-1]

    # Lagged features
    prev_close = latest_data['Close']

    # Prepare input feature array for prediction using fetched sentiments
    X_new = np.array([[latest_sentiment['neg'], latest_sentiment['neu'], latest_sentiment['pos'],
                       daily_return, sma_5, sma_20, rsi, macd,
                       atr, avg_volume_5, prev_close]])

    # Impute missing values using mean strategy (if any remain)
    X_new_imputed = imputer.transform(X_new)

    # Scale features using the same scaler used during training
    X_new_scaled = scaler.transform(X_new_imputed)

    # Make prediction for tomorrow's stock price
    predicted_price = model.predict(X_new_scaled)

    return predicted_price[0]