import pandas as pd
import os
import sqlite3
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def get_vader_sentiment(text):
    if pd.isna(text):
        return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    return analyzer.polarity_scores(text)

if __name__ == "__main__":
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the 'data' directory
    data_dir = os.path.join(script_dir, "..", "data")
    db_path = os.path.join(data_dir, "sentiment.db")

    try:
        conn = sqlite3.connect(db_path)

        # --- Sentiment Analysis for Reddit Data ---
        query_reddit_cleaned = "SELECT id, clean_text, created_at, subreddit FROM cleaned_reddit_posts;"
        reddit_df_cleaned = pd.read_sql(query_reddit_cleaned, conn, index_col='id')

        # Apply VADER sentiment analysis
        reddit_df_cleaned['sentiment_scores'] = reddit_df_cleaned['clean_text'].apply(get_vader_sentiment)
        reddit_df_cleaned['reddit_sentiment'] = reddit_df_cleaned['sentiment_scores'].apply(lambda x: x['compound'])
        reddit_df_cleaned.drop(columns=['sentiment_scores'], inplace=True)

        # Write sentiment scores back to the cleaned_reddit_posts table (replace it)
        reddit_df_cleaned.to_sql("cleaned_reddit_posts", conn, if_exists="replace", index=True)
        print("VADER sentiment scores calculated for Reddit data and updated in cleaned_reddit_posts.")

        # --- Sentiment Analysis for News Data ---
        query_news_cleaned = "SELECT id, clean_text, published_at, company FROM cleaned_news_articles;"
        news_df_cleaned = pd.read_sql(query_news_cleaned, conn, index_col='id')

        # Apply VADER sentiment analysis
        news_df_cleaned['sentiment_scores'] = news_df_cleaned['clean_text'].apply(get_vader_sentiment)
        news_df_cleaned['news_sentiment'] = news_df_cleaned['sentiment_scores'].apply(lambda x: x['compound'])
        news_df_cleaned.drop(columns=['sentiment_scores'], inplace=True)

        # Write sentiment scores back to the cleaned_news_articles table (replace it)
        news_df_cleaned.to_sql("cleaned_news_articles", conn, if_exists="replace", index=True)
        print("VADER sentiment scores calculated for News data and updated in cleaned_news_articles.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()