import sqlite3
import pandas as pd
import os

# Construct the relative path to the database file
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, 'data', 'sentiment.db')

try:
    conn = sqlite3.connect(db_path)

    query_reddit = "SELECT * FROM reddit_posts;"
    reddit_df = pd.read_sql(query_reddit, conn)

    query_news = "SELECT * FROM news_articles;"
    news_df = pd.read_sql(query_news, conn)

    query_stock = "SELECT * FROM stock_prices;"
    stock_df = pd.read_sql(query_stock, conn)

    # --- Cleaning Reddit DataFrame ---
    reddit_df['body'] = reddit_df['body'].fillna('')
    reddit_df['combined_text'] = reddit_df['title'] + ' ' + reddit_df['body']
    reddit_df['created_at'] = pd.to_datetime(reddit_df['created_at'])
    reddit_df.drop(columns=['title', 'body'], inplace=True)
    reddit_df.reset_index(drop=True, inplace=True)

    # Write cleaned reddit_df to a new table
    reddit_df.to_sql('cleaned_reddit_posts', conn, if_exists='replace', index=False)
    print("Cleaned reddit_posts written to the 'cleaned_reddit_posts' table.")

    # --- Cleaning News DataFrame ---
    news_df['description'] = news_df['description'].fillna('')
    news_df['combined_text'] = news_df['title'] + ' ' + news_df['description']
    news_df['published_at'] = pd.to_datetime(news_df['published_at'])
    news_df['scraped_at'] = pd.to_datetime(news_df['scraped_at'])
    news_df.drop(columns=['title', 'description'], inplace=True)
    news_df.reset_index(drop=True, inplace=True)

    # Write cleaned news_df to a new table
    news_df.to_sql('cleaned_news_articles', conn, if_exists='replace', index=False)
    print("Cleaned news_articles written to the 'cleaned_news_articles' table.")

    # --- Cleaning Stock DataFrame ---
    stock_df['date'] = pd.to_datetime(stock_df['date'])

    # Calculate daily percentage change, grouped by ticker
    stock_df['daily_return'] = stock_df.groupby('ticker')['close'].pct_change()

    # Write cleaned stock_df to a new table
    stock_df.to_sql('cleaned_stock_prices', conn, if_exists='replace', index=False)
    print("Cleaned stock_prices written to the 'cleaned_stock_prices' table (with daily return).")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()