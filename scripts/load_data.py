import sqlite3
import pandas as pd
import os

def load_csv_to_db(csv_file, table_name):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Connect to the SQLite database
    # The database file is assumed to be in a directory named 'data' at the same level
    conn = sqlite3.connect(os.path.join("data", "sentiment.db"))

    # Write the DataFrame to the SQL table
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Close the connection
    conn.close()
    print(f"Loaded data into {table_name} from {csv_file}")

# Load data from CSV files into the database
load_csv_to_db(os.path.join("data", "reddit_posts.csv"), "reddit_posts")
load_csv_to_db(os.path.join("data", "news_articles.csv"), "news_articles")
load_csv_to_db(os.path.join("data", "stock_data.csv"), 'stock_prices')