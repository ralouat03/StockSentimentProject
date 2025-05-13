@echo off
REM Batch script to run Phase 1 data pipeline and create sentiment.db

echo Running Reddit scraper...
python scripts\reddit_scraper.py

echo Running NewsAPI scraper...
python scripts\news_scraper.py

echo Running stock data fetcher...
python scripts\stock_fetcher.py

echo Creating SQLite database schema...
python scripts\database.py

echo Loading data into database...
python scripts\load_data.py

echo All Phase 1 tasks completed. sentiment.db is ready.
pause
