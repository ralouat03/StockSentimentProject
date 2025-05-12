# reddit_scraper.py

import praw
import pandas as pd
from datetime import datetime
import os

# Force load .env
from dotenv import load_dotenv
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(script_dir, '.env'))


# API credentials

API_ID = os.getenv('API_ID')
API_SECRET = os.getenv('API_SECRET')
AGENT = os.getenv('AGENT')
USSR = os.getenv('USSR')
PASS = os.getenv('PASS')

# Check if Reddit credentials exist
if not all([API_ID, API_SECRET, AGENT, USSR, PASS]):
    raise ValueError("Missing one or more Reddit API credentials in .env file!")

reddit = praw.Reddit(
    client_id=API_ID,
    client_secret=API_SECRET,
    user_agent=AGENT,
    username=USSR,
    password=PASS
)
# Extract relevant information from subreddits
def scrape_reddit(subreddits, post_limit=50):
    posts = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.hot(limit=post_limit):
            posts.append({
                'subreddit': sub,
                'title': post.title,
                'body': post.selftext,
                'score': post.score,
                'comments': post.num_comments,
                'created_at': datetime.fromtimestamp(post.created_utc)
            })
    return pd.DataFrame(posts)


# Main execution
if __name__ == "__main__":
    try:
        target_subreddits = ['stocks', 'wallstreetbets', 'investing', 'biotechplays', 'defensestocks', 'biotech']
        df = scrape_reddit(target_subreddits)

        if df.empty:
            print("No posts fetched. Check credentials or subreddit accessibility.")
        else:
            print(df.head())

            data_dir = os.path.join(script_dir, "..", "data")
            os.makedirs(data_dir, exist_ok=True)
            output_path = os.path.join(data_dir, "reddit_posts.csv")

            df.to_csv(output_path, index=False)
            print(f"Saved scraped posts to {output_path}")

    except Exception as e:
        print("Error:", e)

    input("Press Enter to exit...")