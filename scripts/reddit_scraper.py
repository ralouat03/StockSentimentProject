import praw
import pandas as pd
from datetime import datetime, timedelta
import os
import time
import requests
from prawcore.exceptions import RequestException, ServerError
from socket import error as SocketError

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# API credentials from .env file
API_ID = os.getenv('API_ID')
API_SECRET = os.getenv('API_SECRET')
AGENT = os.getenv('AGENT')
USSR = os.getenv('USSR')
PASS = os.getenv('PASS')

# Check if Reddit credentials exist
if not all([API_ID, API_SECRET, AGENT, USSR, PASS]):
    raise ValueError("Missing one or more Reddit API credentials in .env file!")

try:
    # Initialize Reddit instance
    print("Initializing Reddit instance...")
    reddit_instance = praw.Reddit(
        client_id=API_ID,
        client_secret=API_SECRET,
        user_agent=AGENT,
        username=USSR,
        password=PASS
    )
except Exception as e:
    print(f"Error initializing Reddit instance: {e}")
    exit()

# Function to scrape Reddit posts within a date range AND intervalled
def scrape_reddit_intervalled(subreddits, start_date, end_date, interval_days=7, posts_per_interval=30, max_retries=3):
    posts = []
    interval = timedelta(days=interval_days)
    current_start = start_date

    while current_start < end_date:
        current_end = min(current_start + interval, end_date)
        print(f"Fetching articles from {current_start} to {current_end}")

        for sub in subreddits:
            retries = 0
            while retries < max_retries:
                try:
                    subreddit = reddit_instance.subreddit(sub)
                    fetched = subreddit.hot(limit=500)  # Overfetch to allow filtering
                    print(f"Fetching articles from subreddit {sub}")

                    count = 0
                    for post in fetched:
                        post_time = datetime.fromtimestamp(post.created_utc)
                        if current_start <= post_time < current_end:
                            posts.append({
                                'subreddit': sub,
                                'title': post.title,
                                'body': getattr(post, 'selftext', ''),
                                'score': post.score,
                                'comments': post.num_comments,
                                'created_at': post_time
                            })
                            count += 1
                            if count >= posts_per_interval:
                                break
                    break
                except (RequestException, ServerError, SocketError, ConnectionResetError, requests.exceptions.RequestException) as e:
                    retries += 1
                    print(f"Retry {retries}/{max_retries} for {sub} ({current_start}–{current_end}): {e}")
                    time.sleep(2 ** retries)
                except Exception as e:
                    print(f"Unexpected error on {sub}: {e}")
                    break
            time.sleep(1.5)
        current_start = current_end
    return pd.DataFrame(posts)

# Main execution
if __name__ == "__main__":
    try:
        target_subreddits = ['stocks', 'wallstreetbets', 'investing', 'biotechplays', 'defensestocks', 'biotech']
        start_date = datetime(2025, 4, 14)
        end_date = datetime(2025, 5, 14)
        df = scrape_reddit_intervalled(target_subreddits, start_date, end_date, interval_days=7, posts_per_interval=30)

        if not df.empty:
            print(df.head())

            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
            os.makedirs(data_dir, exist_ok=True)
            output_path = os.path.join(data_dir, "reddit_posts.csv")

            df.to_csv(output_path, index=False)
            print(f"Saved scraped posts to {output_path}")
        else:
            print("No posts fetched within the specified date range.")

    except Exception as e:
        print(f"Error: {e}")
