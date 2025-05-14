import yfinance as yf
import pandas as pd
import os 

# Define target stock tickers and company names
companies = {
    'PFE': 'Pfizer',
    'MRNA': 'Moderna',
    'LMT': 'Lockheed Martin',
    'RTX': 'Raytheon'
}

# Date range for historical stock data
start_date = '2025-04-01'
end_date = '2025-05-12'

# Store all company data in a list
all_data = []

for ticker, name in companies.items():
    print(f" Fetching data for {name} ({ticker})...")

    # Download historical stock data
    stock = yf.download(ticker, start=start_date, end=end_date)
    stock.reset_index(inplace=True)

    # Filter necessary columns and missing data
    stock = stock[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    stock.dropna(inplace=True)

    # Add moving averages, ticker column, and rearrange
    stock['MA_7'] = stock['Close'].rolling(window=7).mean()
    stock['MA_14'] = stock['Close'].rolling(window=14).mean()
    stock['ticker'] = ticker
    stock = stock[['ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'MA_7', 'MA_14', 'Volume']]

    # Rename columns to match database schema format (lowercase)
    stock.columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'ma_7', 'ma_14', 'volume']

    all_data.append(stock)

# Concatenate all company DataFrames
df = pd.concat(all_data, ignore_index=True)

# Get the directory where the current script is located, and creates path for .csv
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
output_path = os.path.join(data_dir, "stock_data.csv")

# Save the combined DataFrame to a CSV file
df.to_csv(output_path, index=False)
print(f"Stock data (with moving averages) successfully saved to {output_path}")