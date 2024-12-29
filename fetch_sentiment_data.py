import os
import requests
from datetime import datetime, timedelta
import calendar
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Accessing the API key and URL
api_key = os.getenv('EOD_API_TOKEN')
api_url = os.getenv('EOD_API_URL')

# Create an empty list to store descriptions
description_list = []

def fetch_sentiment_data(ticker):
    """
    @Args:- ticker:- str object containing the ticker name of the financial company
    @Description:-
                This method makes a request to the financial model api website and
                fetches the news regarding the ticker.
    @Returns:- description_list:- list object containing all descriptions for the ticker
    """

    # Parse the start date
    start = datetime.strptime('2021-01-01', '%Y-%m-%d')

    # Get yesterday's date(since training data should be upto previous date)
    yesterday = datetime.today() - timedelta(days=1)

    # Initialize current date to the first day of the start month
    current_date = start.replace(day=1)

    while current_date <= yesterday:
        print(current_date, yesterday)
        # Get the last day of the current month
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]

        # Format the start and end dates
        start_of_month = current_date.strftime("%Y-%m-%d")
        end_of_month = current_date.replace(day=last_day).strftime("%Y-%m-%d")

        # Move to the first day of the next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

        response = requests.get(f"{api_url}?s={ticker.upper()}&from={start_of_month}&to={end_of_month}&limit=1000&api_token={api_key}&fmt=json")

        if response.status_code == 200:
            news_data = response.json()
            print(f"Fetched financial sentiment data from {start_of_month} to {end_of_month}")

            for article in news_data:

                # Convert date format from '2024-12-22T12:00:00+00:00' to '23 Aug 2024'
                original_date = article['date']

                # Fixing the timezone format if necessary
                if original_date.endswith('+00:0'):
                    original_date = original_date[:-1] + '00'  # Change '+00:0' to '+00:00'

                # Convert to datetime and format as needed
                try:
                    formatted_date = datetime.fromisoformat(original_date).strftime('%d %b %Y')
                except ValueError as e:
                    print(f"Error parsing date '{original_date}': {e}")
                    continue  # Skip this article if there's an error

                if article.get('sentiment') is not None:
                    # 'sentiment' value should not be None
                    # Create a dictionary for each article with formatted date, title,content and sentiment
                    article_object = {
                        "date": formatted_date,
                        "title": article['title'],
                        "content": article['content'],
                        "sentiment": article['sentiment']
                    }

                    description_list.append(article_object)

        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return description_list