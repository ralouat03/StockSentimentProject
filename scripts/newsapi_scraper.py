import requests
import pandas as pd
from datetime import datetime
import time
import os

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# Check if NewsAPI credentials exist
if not all([API_KEY, BASE_URL]):
    raise ValueError("Missing one or both NewsAPI credentials in .env file!")

# Fetches news article
def fetch_news(company_name):
    params = {
        'q': company_name,          # Keyword to search for
        'language': 'en',           
        'pageSize': 100,            # Max n of results per page
        'sortBy': 'publishedAt',    
        'apiKey': API_KEY
    }

    r = requests.get(BASE_URL, params=params)
    data = r.json()

    # Extract relevant info from articles
    articles = []
    for article in data.get('articles', []):
        articles.append({
            'company': company_name,
            'title': article['title'],
            'description': article['description'],
            'published_at': article['publishedAt'],
            'source': article['source']['name'],
            'url': article['url'],
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    return pd.DataFrame(articles)

# Main execution block
if __name__ == "__main__":
    companies = ['Pfizer', 'Moderna', 'Lockheed Martin', 'Raytheon']
    all_news = []

    for company in companies:
        print(f"Fetching news for {company}...")
        df = fetch_news(company)
        all_news.append(df)
        time.sleep(1.5) # Small delay for API

    result_df = pd.concat(all_news, ignore_index=True)

     # Get the directory where the current script is located (data folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    output_path = os.path.join(data_dir, "news_articles.csv")

    result_df.to_csv(output_path, index=False)
    print(f"News saved to {output_path}")