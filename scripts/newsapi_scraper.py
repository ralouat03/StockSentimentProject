import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# Check if NewsAPI credentials exist
if not all([API_KEY, BASE_URL]):
    raise ValueError("Missing one or both NewsAPI credentials in .env file!")

def fetch_news_single_page(company_name, from_date, to_date, page=1):
    params = {
        'q': company_name,          # Keyword to search for
        'language': 'en',
        'pageSize': 100,             # Max n of results per page
        'sortBy': 'publishedAt',
        'apiKey': API_KEY,
        'from': from_date.strftime('%Y-%m-%d'),
        'to': to_date.strftime('%Y-%m-%d'),
        'page': page
    }

    try:
        r = requests.get(BASE_URL, params=params)
        data = r.json()
        articles = []
        if data.get('status') == 'ok':
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
        else:
            print(f"Error fetching news for {company_name} ({from_date} to {to_date}), page {page}: {data.get('message')}")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Request error for {company_name} ({from_date} to {to_date}), page {page}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    companies = ['Pfizer', 'Moderna', 'Lockheed Martin', 'Raytheon']
    all_news = []
    start_date_str = '2025-04-16'
    end_date_str = '2025-05-12'
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    date_increment = timedelta(days=32) # Fetch for the entire range in one go

    for company in companies:
        print(f"Fetching news for {company} from {start_date} to {end_date} (first 100 results)...")
        df = fetch_news_single_page(company, start_date, end_date, page=1)
        if not df.empty:
            all_news.append(df)
        time.sleep(1.5) # Respect API rate limits

    if all_news:
        result_df = pd.concat(all_news, ignore_index=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..", "data")
        output_path = os.path.join(data_dir, "news_articles.csv")

        result_df.to_csv(output_path, index=False)
        print(f"First 100 news articles per company within the specified timeframe saved to {output_path}")
    else:
        print("No news articles fetched within the specified timeframe.")