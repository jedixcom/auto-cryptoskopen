import json
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os
import logging
from datetime import datetime, timezone
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB connection setup
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("Missing environment variable MONGO_URI")

logging.debug(f"Attempting to connect to MongoDB with URI: {mongo_uri}")
try:
    client = pymongo.MongoClient(mongo_uri)
    db = client["cryptoskopen-eu"]
    input_collection = db["in"]
    logging.debug("MongoDB connection successful")
except pymongo.errors.ConnectionError as e:
    logging.error(f"MongoDB connection failed: {e}")
    raise

# User-Agent rotation
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
]

def fetch_article_details(link, retries=3, backoff_factor=2):
    """Fetches article details from a given link, with retry logic."""
    for attempt in range(retries):
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://cointelegraph.com/',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1'
            }
            logging.debug(f"Fetching article details from {link}")
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            logging.debug(f"Successfully fetched article details from {link}")
            full_text, body, image_url = extract_article_details(response.text)
            return full_text, body, image_url

        except requests.exceptions.RequestException as e:
            logging.warning(f"Error fetching URL: {link}. Attempt: {attempt+1}. Error: {e}")
            if attempt < retries - 1:  # Wait before retrying
                sleep_time = backoff_factor ** attempt
                logging.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)

    return None, None, None  # Return None for all values if all attempts fail

def extract_article_details(html_content):
    """Extracts full text, body and image URL from the HTML content of an article."""
    try:
        logging.debug("Extracting article details from HTML content")
        soup = BeautifulSoup(html_content, 'html.parser')

        article_body = soup.find('div', class_='post-content')
        full_text = article_body.get_text(separator='\n').strip() if article_body else "Full text not found."

        body = article_body.get_text(separator=' ') if article_body else "Body text not found."

        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image and og_image['content'] else "https://example.com/default-image.jpg"

        return full_text, body, image_url

    except Exception as e:
        logging.error(f"Error extracting article details: {e}")
        return "Full text not found.", "Body text not found.", "https://example.com/default-image.jpg"

def get_latest_article_date():
    """Retrieves the publication date of the most recent article from the database."""
    logging.debug("Fetching the latest article date from the database")
    latest_article = input_collection.find_one(sort=[("published", pymongo.DESCENDING)])
    if latest_article:
        logging.debug(f"Latest article date found: {latest_article['published']}")
        return datetime.strptime(latest_article["published"], "%a, %d %b %Y %H:%M:%S %z")
    logging.debug("No articles found in the database")
    return None

def run_script(feed_path, num_articles, category):
    """Main function to fetch, parse, and store RSS feed articles."""
    logging.info(f"Parsing RSS feed from {feed_path}")
    with open(feed_path, 'r') as f:
        feed = json.load(f)

    latest_article_date = get_latest_article_date()

    count = 0
    for entry in feed['entries']:
        if count >= num_articles:
            break

        published = datetime.strptime(entry['published'], "%a, %d %b %Y %H:%M:%S %z")

        if not latest_article_date or published > latest_article_date:
            existing_article = input_collection.find_one({"link": entry['link']})
            if existing_article:
                logging.info(f"Article '{entry['title']}' already exists in the database.")
                continue

            full_text, body, image_url = fetch_article_details(entry['link'])

            if full_text and body and image_url:
                article = {
                    "title": entry['title'],
                    "link": entry['link'],
                    "published": entry['published'],
                    "summary": entry['description'],
                    "full_text": full_text,
                    "body": body,
                    "image_url": image_url,
                    "category": category if category else None,
                    "processed": False
                }
                try:
                    input_collection.insert_one(article)
                    logging.info(f"Saved article '{entry['title']}' to MongoDB.")
                    count += 1
                except pymongo.errors.PyMongoError as e:
                    logging.error(f"Failed to save article '{entry['title']}' to MongoDB. Error: {e}")
            else:
                logging.warning(f"Failed to fetch article details for '{entry['title']}'. Skipping...")

    logging.info(f"{count} new RSS news articles have been saved to the 'news_rewrite.in' collection in MongoDB.")

def main():
    feed_path = './feed.json'
    num_articles = 3
    category = None

    run_script(feed_path, num_articles, category)

if __name__ == "__main__":
    main()