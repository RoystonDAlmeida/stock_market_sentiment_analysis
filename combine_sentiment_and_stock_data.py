import pandas as pd

def get_combined_sentiment_and_stock_data(sentiment_description_list,sentiments_list, stock_data):
    """
    @Args:- sentiment_description_list:- list object containing sentiment of the form('date', 'title', 'content'),
            sentiments_list:- list object containing sentiment of each sentiment 'content,
            stock_data:- dataframe object containing stock data
    @Description:-
                This method combines sentiment of each sentiment content and stock data
    @Returns:- combined_data:- dataframe object that combines stock_data and sentiments_list
    """

    # Create a Dataframe for sentiment scores with timestamps
    sentiment_df = pd.DataFrame(sentiments_list)
    # print(sentiment_df)
    # print(f"Length of sentiments_list: {len(sentiments_list)}")
    # print(f"Length of sentiment_description_list: {len(sentiment_description_list)}")

    sentiment_df['date'] = pd.to_datetime([sentiment_description['date']
                                           for sentiment_description in sentiment_description_list])
    sentiment_df['compound'] = sentiment_df['compound'].apply(lambda x:-1 if x>0 else {-1 if x<0 else 0})

    # Group by date and calculate mean for numeric columns
    grouped_sentiment = sentiment_df.groupby('date').mean(numeric_only=True).reset_index()

    # Check if stock_data has a MultiIndex and flatten it if necessary
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)  # Flatten to first level

    # Merge with stock price data on date
    stock_data.reset_index(inplace=True)

    combined_data = pd.merge(stock_data[['Date', 'Close', 'High', 'Low', 'Volume']], grouped_sentiment,
                             left_on='Date', right_on='date', how='inner')
    # print(combined_data)
    return combined_data