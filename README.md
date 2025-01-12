# 📊 Stock Market Sentiment Analysis

## 🌟 Overview

This project implements a stock market sentiment analysis tool using Python. It analyzes news headlines and social media posts to gauge market sentiment, providing valuable insights for investors and traders.

## ✨ Features

- 📰 Fetches real-time stock news from various sources
- 🧠 Performs sentiment analysis on news headlines and social media posts
- 📈 Visualizes sentiment trends over time
- 💹 Provides sentiment scores for individual stocks and overall market

## 🛠️ Prerequisites

- Python 3.7+
- pip

## 🚀 Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:RoystonDAlmeida/stock_market_sentiment_analysis.git
    cd stock_market_sentiment_analysis/
    ```

2. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Usage

To run the Streamlit app locally:

```bash
streamlit run app.py
```

This will start the app and open it in your default web browser. If it doesn't open automatically, you can access it at `http://localhost:8501`.
Follow the prompt to input stock ticker symbols

## ⚙️ Configuration

Add the following values to `.env`:-

- `EOD_API_TOKEN = `
- `EOD_API_URL = `

## 📁 File Structure

```bash
stock_market_sentiment_analysis/
│
├── app.py
├── combine_sentiment_and_stock_data.py
├── fetch_sentiment_data.py
├── get_last_trading_day_price.py
├── perform_sentiment_analysis.py
├── predict_next_trading_day_price.py
├── preprocess_text.py
├── README.md
├── requirements.txt
├── stock_price_data.py
├── stock_price_plotter.py
├── trading_day_price_fetcher.py
└── train_machine_learning_model.py
```


## 📚 Libraries Used

- Streamlit: Web app framework for machine learning and data science projects
- NLTK: Natural Language Toolkit for text processing
- VADER: Sentiment analysis tool optimized for social media
- Pandas: Data manipulation and analysis
- Plotly: Interactive data visualization
- yfinance: Package for historical stock data
- scikit-learn: To train the model

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See [LICENSE](https://opensource.org/license/MIT) for more information.

## 🙏 Acknowledgments

- [EOD Historical Data](https://eodhd.com/) for sentiment analysis and financial news data
- [yfinance](https://github.com/ranaroussi/yfinance) for additional stock data