import feedparser
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os

# Load MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("Missing environment variable MONGO_URI")

print("Connecting to MongoDB...")
# Connect to MongoDB using the URI from the environment variable
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client["cryptoskopen-eu"]
    input_collection = db["in"]
    output_collection = db["rw"]
    print("Connected to MongoDB successfully.")
except pymongo.errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB. Error: {e}")
    raise

# Function to fetch article details
def fetch_article_details(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        print(f"Fetching article details from {link}...")
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            print(f"Successfully fetched article details from {link}.")
            full_text, image_url = extract_article_details(response.text)
            return full_text, image_url
        else:
            print(f"Failed to fetch article details from {link}. Status code: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch article details from {link}. Exception: {e}")
        return None, None

# Function to extract full text and image URL from HTML content
def extract_article_details(html_content):
    try:
        print("Extracting article details from HTML content...")
        soup = BeautifulSoup(html_content, 'html.parser')
        article_body = soup.find('div', class_='post-content')
        full_text = article_body.get_text(separator='\n').strip() if article_body else "Full text not found."
        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image and og_image['content'] else "https://example.com/default-image.jpg"
        return full_text, image_url
    except Exception as e:
        print(f"Error extracting article details: {e}")
        return "Full text not found.", "https://example.com/default-image.jpg"

def run_script(rss_feed_url, num_articles, category):
    print(f"Parsing RSS feed from {rss_feed_url}...")
    feed = feedparser.parse(rss_feed_url)

    count = 0
    for entry in feed.entries:
        if count >= num_articles:
            break

        # Check if the article already exists
        print(f"Checking if article '{entry.title}' already exists in the database...")
        existing_article = input_collection.find_one({"link": entry.link})
        if existing_article:
            print(f"Article '{entry.title}' already exists in the database.")
            continue  # Skip to the next entry

        attempts = 3
        while attempts > 0:
            full_text, image_url = fetch_article_details(entry.link)
            if full_text and image_url:
                article = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "summary": entry.summary,
                    "full_text": full_text,
                    "image_url": image_url,
                    "category": category if category else None,
                    "processed": False  # Set processed to False initially
                }
                try:
                    input_collection.insert_one(article)
                    print(f"Saved article '{entry.title}' to MongoDB.")
                    count += 1
                    break
                except pymongo.errors.PyMongoError as e:
                    print(f"Failed to save article '{entry.title}' to MongoDB. Error: {e}")
                    attempts -= 1
                    time.sleep(5)
            else:
                attempts -= 1
                time.sleep(5)

        if attempts == 0:
            print(f"Failed to fetch and save article '{entry.title}' after multiple attempts.")

    print(f"{count} RSS news articles have been saved to the 'news_rewrite.in' collection in MongoDB.")

def main():
    rss_feed_url = 'https://cointelegraph.com/rss'
    num_articles = 3  # Set the desired number of articles to fetch
    category = None  # Set the desired category if needed

    print("Starting the script...")
    run_script(rss_feed_url, num_articles, category)
    print("Script finished.")

if __name__ == "__main__":
    main()