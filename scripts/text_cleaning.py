import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.punkt import PunktSentenceTokenizer
import os

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
try: 
    PunktSentenceTokenizer()
except LookupError:
    nltk.download('punkt')

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
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return " ".join(filtered)

if __name__ == "__main__":
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the 'data' directory (one level up from 'scripts')
    data_dir = os.path.join(script_dir, "..", "data")

    # Construct the full paths for the input and output CSV files
    reddit_input_path = os.path.join(data_dir, "reddit_posts.csv")
    news_input_path = os.path.join(data_dir, "news_articles.csv")
    reddit_output_path = os.path.join(data_dir, "reddit_cleaned.csv")
    news_output_path = os.path.join(data_dir, "news_cleaned.csv")

    # Load CSVs
    reddit_df = pd.read_csv(reddit_input_path)
    news_df = pd.read_csv(news_input_path)

# Combine relevant columns into a single text column
reddit_df["text"] = reddit_df["title"].fillna('') + " " + reddit_df["body"].fillna('')
news_df["text"] = news_df["title"].fillna('') + " " + news_df["description"].fillna('')

# Clean text
reddit_df["clean_text"] = reddit_df["text"].apply(clean_text)
news_df["clean_text"] = news_df["text"].apply(clean_text)

# Save cleaned files
reddit_df.to_csv(reddit_output_path, index=False)
news_df.to_csv(news_output_path, index=False)

print("Cleaned text saved to reddit_cleaned.csv and news_cleaned.csv")
