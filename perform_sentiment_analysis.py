import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Using the pre-trained VADER model for sentiment analysis
nltk.download('vader_lexicon')

# Add an empty sentiments_list to store('neg', 'neu', ;pos')
sentiments_list = []

# Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def get_sentiments_list(sentiment_description_list):
    """
    @Args:- sentiment_description_list:- list object containing various sentiment descriptions
    @Description:-
                This method performs sentiment analysis on each description in the sentiment_description_list
    @Returns:- sentiments_list:- list object containing sentiment of each description
    """

    for description in sentiment_description_list:

        combined_score = {
            'compound':description['sentiment']['polarity'],
            'neg':description['sentiment']['neg'],
            'neu':description['sentiment']['neu'],
            'pos':description['sentiment']['pos']
        }

        sentiments_list.append(combined_score)

    return sentiments_list