import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

if not all([API_KEY, BASE_URL]):
    raise ValueError("Missing one or both NewsAPI credentials in .env file!")

def fetch_news_single_page(company_name, from_date, to_date, page=1):
    params = {
        'q': company_name,
        'language': 'en',
        'pageSize': 100,
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

    range_start = datetime.strptime('2025-04-15', '%Y-%m-%d').date()
    range_end = datetime.strptime('2025-05-14', '%Y-%m-%d').date()
    interval = timedelta(days=8)

    for company in companies:
        current_start = range_start
        while current_start < range_end:
            current_end = min(current_start + interval, range_end)
            print(f"Fetching news for {company} from {current_start} to {current_end}...")
            df = fetch_news_single_page(company, current_start, current_end)
            if not df.empty:
                all_news.append(df)
            time.sleep(1.5)
            current_start = current_end

    if all_news:
        result_df = pd.concat(all_news, ignore_index=True)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        output_path = os.path.join(data_dir, "news_articles.csv")
        result_df.to_csv(output_path, index=False)
        print(f"News articles saved to {output_path}")
    else:
        print("No news articles fetched within the specified timeframe.")
