import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Using the pre-trained VADER model for sentiment analysis
nltk.download('vader_lexicon')

# Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def get_sentiments_list(sentiment_description_list):
    """
    @Args:- sentiment_description_list:- list object containing various sentiment descriptions
    @Description:-
                This method performs sentiment analysis on each description in the sentiment_description_list
    @Returns:- sentiments_list:- list object containing sentiment of each description
    """

    sentiments_list = [sia.polarity_scores(description['content']) for description in sentiment_description_list]
    return sentiments_list