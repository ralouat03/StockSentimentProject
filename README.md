# Real-Time Social Sentiment Analysis for Stock Prediction

## Overview

This project establishes an end-to-end pipeline to collect, process, and structure real-time social and news sentiment data with the goal of predicting short-term stock market movements. It focuses on pharmaceutical and defense sector stocks, specifically Pfizer, Moderna, Lockheed Martin, and Raytheon. This README details, first, how to run, then, the phases of the project to its completion.

## How to Run 

(IMPORTANT) In order to replicate getting 'sentiment.db', users must provide their own API credentials by creating a `.env` file in the project root. A template in the root is provided as `.env.example`. Edit, and insert valid API keys.
You must also create a **data** folder in the repo folder (as a sibling to the scripts folder)

Then, run `run_phase1.bat` & `run_phase2.bat`

You now have a `sentiment.db` :)

---

# Phase 1: Data Collection

## Objectives
- Scrape social sentiment and news data related to selected companies.
- Retrieve historical stock market data.
- Clean, format, and store all data in a unified SQLite database (`sentiment.db`).
- Create an accompanying JuypterNotebook with Phase 1


---

## Data Sources

### Reddit
Used PRAW (Python Reddit API Wrapper) to extract hot posts from subreddits:
- `stocks`
- `wallstreetbets`
- `investing`
- `biotechplays`
- `defensestocks`
- `biotech`

Each post includes:  
- `subreddit`, `title`, `body`, `score`, `num_comments`, `created_at`

Script: `reddit_scraper.py`  
Output: `data/reddit_posts.csv`

### NewsAPI
Used NewsAPI to pull recent articles for:
- Pfizer
- Moderna
- Lockheed Martin
- Raytheon

Each article includes:  
- `title`, `description`, `published_at`, `source`, `url`, `scraped_at`

Script: `news_scraper.py`  
Output: `data/news_articles.csv`

### Financial Data (Yahoo Finance)
Used `yfinance` to retrieve OHLCV data and compute 7-day and 14-day moving averages.

Tickers:
- `PFE` (Pfizer)
- `MRNA` (Moderna)
- `LMT` (Lockheed Martin)
- `RTX` (Raytheon)

Each row includes:  
- `ticker`, `date`, `open`, `high`, `low`, `close`, `ma_7`, `ma_14`, `volume`

Script: `stock_fetcher.py`  
Output: `data/stock_data.csv`

---

## Database Setup

### Schema
Created using `schema.sql` and initialized via `database.py`.

Tables:
- `reddit_posts`
- `news_articles`
- `stock_prices`

### Data Loading
All CSV outputs loaded into the database using `load_data.py`.

Database file: `data/sentiment.db`  
Tool used for inspection: **DB Browser for SQLite**

---

## Security & Portability
- `.env` file used for API credentials
- `.gitignore` implemented to exclude sensitive files
- All file paths use relative references to ensure cross-environment compatibility

---
# Phase 2: Data Processing and Sentiment Analysis

## Objectives

This phase of the project focuses on processing the raw data collected in Phase 1 to prepare it for sentiment analysis and subsequent analysis in Power BI. The primary objectives are:

* **Data Cleaning and Transformation:** Perform initial cleaning and transformation of the raw data from various sources (stock prices, news articles, Reddit posts) to ensure consistency and usability.
* **Sentiment Analysis:** Apply Natural Language Processing (NLP) techniques to extract sentiment scores from the text data (news articles and Reddit posts).
* **Data Integration:** Store the processed and sentiment-annotated data in a structured format (SQLite database) to facilitate further analysis.
* **Export for Visualization:** Export the processed data to a format suitable for visualization and analysis in Power BI.

## Scripts

This phase involves the following Python scripts:

* **`preprocess_data.py`**
    * **Functionality:** This script performs initial cleaning and transformation of the raw data.
    * Specifically, it processes the raw data from the stock price data.
    * It writes the cleaned and transformed data to new tables within the `sentiment.db` SQLite database.
    * **Key Actions:**
        * Loads raw data (e.g., from CSV files).
        * Cleans data (e.g., handles missing values, converts data types).
        * Transforms data (e.g., calculates daily returns for stock prices).
        * Creates new tables in the `sentiment.db` database (if they don't exist) and writes the processed data to these tables.

* **`clean_sentiment_text.py`**
    * **Functionality**: This script uses Natural Language Processing (NLP) to process the text data from news articles and Reddit posts to prepare it for sentiment analysis.
    * **Key Actions**:
        * Loads raw text data from the `sentiment.db` database (specifically, from tables containing news article and Reddit post data).
        * Performs text cleaning (e.g., removing punctuation, stop words, HTML tags).
        * Writes the cleaned text data back to the `sentiment.db` database, typically to new tables (e.g., `cleaned_news_articles`, `cleaned_reddit_posts`).

* **`calculate_sentiment.py`**
    * **Functionality:** This script applies the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis tool to the cleaned text data.
    * **Key Actions:**
        * Loads the cleaned text data from the `sentiment.db` database (from the tables created by `clean_sentiment_text.py`).
        * Calculates sentiment scores (positive, negative, neutral, compound) for each text item (news article, Reddit post) using VADER.
        * Writes the sentiment scores back to the `sentiment.db` database, typically to the same tables as the cleaned text (e.g., adding new columns for sentiment scores).
    
## Data Export to Power BI

After the scripts have been executed, the `sentiment.db` SQLite database contains the processed data, including sentiment scores. To analyze this data in Power BI, the following steps were taken:

1.  **Connect Power BI to SQLite:** Power BI Desktop was used to connect to the `sentiment.db` database using the SQLite ODBC driver.
2.  **Import Tables:** The relevant tables from `sentiment.db` (e.g., cleaned stock prices, news articles with sentiment, Reddit posts with sentiment) were imported into the Power BI data model.
3.  **Relationships:** Relationships were defined between the tables in Power BI (e.g., linking stock prices to news articles and Reddit posts based on date and ticker symbol where applicable).
4.  **Data Transformation (in Power BI):** Any necessary data transformations or calculations specific to Power BI were performed (e.g., creating calculated columns, defining measures).
5.  **Visualization and Analysis:** Power BI's visualization tools were used to create charts, graphs, and dashboards to explore the relationships between stock prices and sentiment derived from news and social media data.
6.  **Export as CSV (Alternative):** As an alternative, the data from the `sentiment.db` database could also be exported to CSV files using Python (with the `pandas` library) and then imported into Power BI.  However, connecting directly to the database is generally preferred for larger datasets.



