# Market Sentiment & Volatility Analyzer

### 🚀 Executive Summary
An end-to-end data engineering and analytics pipeline that quantifies the correlation between social/news sentiment and short-term stock volatility. Focused on high-sensitivity sectors (Pharma & Defense), this tool ingests unstructured text data, processes it via NLP (VADER), and maps sentiment polarity against OHLCV market data to identify potential alpha generation signals.

**Target Assets:** Pfizer (PFE), Moderna (MRNA), Lockheed Martin (LMT), Raytheon (RTX).

---

### 🛠 Technical Architecture
**Status:** `v1.0 (Complete)`

| Component | Tech Stack |
| :--- | :--- |
| **Ingestion** | Python (`PRAW`, `NewsAPI`, `yfinance`) |
| **ETL Pipeline** | Pandas, NumPy, SQLite |
| **NLP Engine** | `NLTK`, `VADER` (Lexicon-based sentiment scoring) |
| **Storage** | SQLite (Relational Database) |
| **Visualization** | Power BI (via ODBC connection) |

---

### 📊 Key Features
1.  **Multi-Source Ingestion:** Simultaneously scrapes Reddit (retail sentiment) and global news (institutional sentiment) to create a weighted sentiment index.
2.  **Automated ETL:** Python scripts normalize unstructured JSON/HTML data into a structured Relational Database Schema (`sentiment.db`).
3.  **Volatility Mapping:** Calculates 7-day and 14-day Moving Averages (MA) to correlate sentiment spikes with price action.
4.  **Enterprise Security:** Implements `.env` for API key management and `.gitignore` protocols to ensure zero-trust security compliance.

---

### 📂 Repository Structure
```bash
├── data/                   # Local storage for CSVs and SQLite DB
├── scripts/
│   ├── ingestion/          # Scrapers (reddit_scraper.py, news_scraper.py)
│   ├── processing/         # NLP & Cleaning (clean_sentiment_text.py)
│   ├── storage/            # SQL Schema & Loading (database.py)
│   └── analysis/           # VADER Logic (calculate_sentiment.py)
├── notebooks/              # Jupyter Notebooks for EDA
├── requirements.txt        # Python dependencies
└── README.md
