import feedparser
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB connection setup
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("Missing environment variable MONGO_URI")

client = pymongo.MongoClient(mongo_uri)
db = client["cryptoskopen-eu"]
input_collection = db["in"]
output_collection = db["rw"]

def fetch_article_details(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    proxies = {
        # Replace with your proxy settings if needed
        # 'http': 'http://yourproxy:port',
        # 'https': 'http://yourproxy:port',
    }
    try:
        logging.debug(f"Fetching article details from {link}")
        response = requests.get(link, headers=headers, proxies=proxies)
        if response.status_code == 200:
            logging.debug(f"Successfully fetched article details from {link}")
            full_text, image_url = extract_article_details(response.text)
            return full_text, image_url
        elif response.status_code == 403:
            logging.warning(f"Access denied (403) for {link}. Retrying...")
            time.sleep(5)  # Wait before retrying
            response = requests.get(link, headers=headers, proxies=proxies)
            if response.status_code == 200:
                logging.debug(f"Successfully fetched article details from {link} on retry")
                full_text, image_url = extract_article_details(response.text)
                return full_text, image_url
            else:
                logging.warning(f"Failed to fetch article details from {link}. Status code: {response.status_code}")
                return None, None
        else:
            logging.warning(f"Failed to fetch article details from {link}. Status code: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch article details from {link}. Exception: {e}")
        return None, None

def extract_article_details(html_content):
    try:
        logging.debug("Extracting article details from HTML content")
        soup = BeautifulSoup(html_content, 'html.parser')
        article_body = soup.find('div', class_='post-content')
        full_text = article_body.get_text(separator='\n').strip() if article_body else "Full text not found."
        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image and og_image['content'] else "https://example.com/default-image.jpg"
        return full_text, image_url
    except Exception as e:
        logging.error(f"Error extracting article details: {e}")
        return "Full text not found.", "https://example.com/default-image.jpg"

def get_latest_article_date():
    logging.debug("Fetching the latest article date from the database")
    latest_article = input_collection.find_one(sort=[("published", pymongo.DESCENDING)])
    if latest_article:
        logging.debug(f"Latest article date found: {latest_article['published']}")
        return datetime.strptime(latest_article["published"], "%a, %d %b %Y %H:%M:%S %z")
    logging.debug("No articles found in the database")
    return None

def run_script(rss_feed_url, num_articles, category):
    logging.info(f"Parsing RSS feed: {rss_feed_url}")
    feed = feedparser.parse(rss_feed_url)
    latest_article_date = get_latest_article_date()

    count = 0
    for entry in feed.entries:
        if count >= num_articles:
            break

        published = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")

        if not latest_article_date or published > latest_article_date:
            existing_article = input_collection.find_one({"link": entry.link})
            if existing_article:
                logging.info(f"Article '{entry.title}' already exists in the database.")
                continue

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
                        "processed": False
                    }
                    try:
                        input_collection.insert_one(article)
                        logging.info(f"Saved article '{entry.title}' to MongoDB.")
                        count += 1
                        break
                    except pymongo.errors.PyMongoError as e:
                        logging.error(f"Failed to save article '{entry.title}' to MongoDB. Error: {e}")
                        attempts -= 1
                        time.sleep(5)
                else:
                    attempts -= 1
                    time.sleep(5)

            if attempts == 0:
                logging.warning(f"Failed to fetch and save article '{entry.title}' after multiple attempts.")
    logging.info(f"{count} new RSS news articles have been saved to the 'news_rewrite.in' collection in MongoDB.")

def main():
    rss_feed_url = 'https://cointelegraph.com/rss'
    num_articles = 1
    category = None

    run_script(rss_feed_url, num_articles, category)

if __name__ == "__main__":
    main()