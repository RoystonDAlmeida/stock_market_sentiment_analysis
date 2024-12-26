import os
import requests
from datetime import datetime
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

    response = requests.get(f"{api_url}?s={ticker.upper()}&offset=0&limit=100&&api_token={api_key}&fmt=json")

    if response.status_code == 200:
        news_data = response.json()

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

            # Create a dictionary for each article with formatted date, title, and content
            article_object = {
                "date": formatted_date,
                "title": article['title'],
                "content": article['content']
            }

            description_list.append(article_object)

    else:
        print(f"Failed to retrieve data: {response.status_code}")

    return description_list