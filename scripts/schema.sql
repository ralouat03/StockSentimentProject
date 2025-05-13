CREATE TABLE IF NOT EXISTS reddit_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subreddit TEXT,
    title TEXT,
    body TEXT,
    score INTEGER,
    comments INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    title TEXT,
    description TEXT,
    published_at TEXT,
    source TEXT,
    url TEXT,
    scraped_at TEXT
);

CREATE TABLE IF NOT EXISTS stock_prices (
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    ma_7 REAL,
    ma_14 REAL,
    volume INTEGER
);