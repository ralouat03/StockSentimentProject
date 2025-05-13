# Real-Time Social Sentiment Analysis for Stock Prediction

## Overview

This project establishes an end-to-end pipeline to collect, process, and structure real-time social and news sentiment data with the goal of predicting short-term stock market movements. It focuses on pharmaceutical and defense sector stocks, specifically Pfizer, Moderna, Lockheed Martin, and Raytheon.

---

## Phase 1: Data Collection

### Objectives
- Scrape social sentiment and news data related to selected companies.
- Retrieve historical stock market data.
- Clean, format, and store all data in a unified SQLite database (`sentiment.db`).
- Create an accompanying JuypterNotebook with Phase 1

### How to Run 

(IMPORTANT) In order to replicate getting 'sentiment.db', users must provide their own API credentials by creating a `.env` file in the project root. A template in the root is provided as `.env.example`. Edit, and insert valid API keys.

Then, run `run_phase1.bat`

You now have `sentiment.db` :)
---

### Data Sources

#### Reddit
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

#### NewsAPI
Used NewsAPI to pull recent articles for:
- Pfizer
- Moderna
- Lockheed Martin
- Raytheon

Each article includes:  
- `title`, `description`, `published_at`, `source`, `url`, `scraped_at`

Script: `news_scraper.py`  
Output: `data/news_articles.csv`

#### Financial Data (Yahoo Finance)
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

### Database Setup

#### Schema
Created using `schema.sql` and initialized via `database.py`.

Tables:
- `reddit_posts`
- `news_articles`
- `stock_prices`

#### Data Loading
All CSV outputs loaded into the database using `load_data.py`.

Database file: `data/sentiment.db`  
Tool used for inspection: **DB Browser for SQLite**

---

### Security & Portability
- `.env` file used for API credentials
- `.gitignore` implemented to exclude sensitive files
- All file paths use relative references to ensure cross-environment compatibility

---

### Status
Phase 1 completed. All source data is structured, cleaned, and centralized in `sentiment.db`.

