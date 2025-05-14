import praw
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_SECRET = os.getenv('API_SECRET')
AGENT = os.getenv('AGENT')
USSR = os.getenv('USSR')
PASS = os.getenv('PASS')

try:
    reddit = praw.Reddit(
        client_id=API_ID,
        client_secret=API_SECRET,
        user_agent=AGENT,
        username=USSR,
        password=PASS
    )
    print("Successfully connected to Reddit via PRAW")
    # Try a simple API call
    subreddit = reddit.subreddit("python")
    print(f"Connected to subreddit: {subreddit.display_name}")
except Exception as e:
    print(f"Error connecting to Reddit: {e}")