import yfinance as yf
from datetime import datetime, timedelta

# Function to get company name from ticker
def get_company_name(ticker_name):
    """
    @Args:- ticker_name:- str object containing the ticker name
    @Description:-
                This method gets the company name corresponding to a ticker name
    @Returns:- longName:- str object containing company name
    """
    stock = yf.Ticker(ticker_name)
    company_name = stock.info.get('longName')

    if not company_name:
        raise ValueError("Company name not found for the given ticker.")

    return company_name

# Step 1.1: Gather Stock Price Data
def get_stock_data_and_rows(ticker_name):
    """
    @Args:- ticker_name:- str object that contains the stock ticker name
    @Description:-
                This function gets the stock data dataframe head  corresponding
                to the company and the company name
    @Returns:-  stock_data:- dataframe containing historical stock data(upto today's date),
                stock_data.head():- head portion of the stock_data dataframe,
                company_name:- str object containing the company name from ticker name
    """

    # Format the last trading date(upto yesterday or previous day) date as 'yyyy-mm-dd'
    yesterday_date = datetime.today() - timedelta(days=1)
    formatted_date = yesterday_date.strftime('%Y-%m-%d')

    # Download stock data(Start from 2024-01-01) upto last trading day(yesterday)
    stock_data = yf.download(ticker_name, start='2024-01-01', end=formatted_date)

    # Getting the total number of rows present in stock_data
    total_rows = stock_data.shape[0]  # or use len(stock_data)

    return stock_data, stock_data.head(), total_rows