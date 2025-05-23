@echo off

echo Running Reddit scraper...
python scripts\reddit_scraper.py
echo Reddit scraper finished. Press Enter to continue...
pause > nul

echo Running NewsAPI scraper...
python scripts\newsapi_scraper.py
echo NewsAPI scraper finished. Press Enter to continue...
pause > nul

echo Running stock data fetcher...
python scripts\stock_fetcher.py
echo Stock data fetcher finished. Press Enter to continue...
pause > nul

echo Creating SQLite database schema...
python scripts\database.py
echo Database schema created. Press Enter to continue...
pause > nul

echo Loading data into database...
python scripts\load_data.py
echo Data loaded into database. Press Enter to continue...
pause > nul

echo All Phase 1 tasks completed. sentiment.db is ready.
pause