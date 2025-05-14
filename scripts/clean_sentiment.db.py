import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import sqlite3

# Download required NLTK resources (run once)
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    word_tokenize("example")
except LookupError:
    nltk.download('punkt')
try:
    WordNetLemmatizer().lemmatize("example")
except LookupError:
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Text cleaning function
def clean_text(text):
    if pd.isna(text):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs and special characters
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words("english"))
    filtered = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return " ".join(filtered)

if __name__ == "__main__":
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the 'data' directory
    data_dir = os.path.join(script_dir, "..", "data")
    db_path = os.path.join(data_dir, "sentiment.db")

    try:
        conn = sqlite3.connect(db_path)

        # --- Clean Reddit Data ---
        query_reddit = "SELECT id, subreddit, title, body, created_at FROM reddit_posts;"
        reddit_df = pd.read_sql(query_reddit, conn)

        # Combine relevant columns into a single text column
        reddit_df["combined_text"] = reddit_df["title"].fillna('') + " " + reddit_df["body"].fillna('')

        # Clean text
        reddit_df["clean_text"] = reddit_df["combined_text"].apply(clean_text)

        # Select the columns we want in the cleaned table - ENSURE 'created_at' IS INCLUDED
        reddit_df_cleaned = reddit_df[['id', 'subreddit', 'created_at', 'combined_text', 'clean_text']]

        # Write to the cleaned_reddit_posts table (replace if exists)
        reddit_df_cleaned.to_sql("cleaned_reddit_posts", conn, if_exists="replace", index=False)
        print("Cleaned Reddit text processed and saved to cleaned_reddit_posts (with created_at and subreddit).")

        # --- Clean News Data ---
        query_news = "SELECT id, company, title, description, published_at FROM news_articles;"
        news_df = pd.read_sql(query_news, conn)

        # Combine relevant columns
        news_df["combined_text"] = news_df["title"].fillna('') + " " + news_df["description"].fillna('')

        # Clean text
        news_df["clean_text"] = news_df["combined_text"].apply(clean_text)

        # Select columns for cleaned table - ENSURE 'published_at' IS INCLUDED
        news_df_cleaned = news_df[['id', 'company', 'published_at', 'combined_text', 'clean_text']]

        # Write to the cleaned_news_articles table (replace if exists)
        news_df_cleaned.to_sql("cleaned_news_articles", conn, if_exists="replace", index=False)
        print("Cleaned News text processed and saved to cleaned_news_articles (with published_at).")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()