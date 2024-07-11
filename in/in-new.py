import feedparser
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os
from datetime import datetime

# Load MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("Missing environment variable MONGO_URI")

# Connect to MongoDB using the URI from the environment variable
client = pymongo.MongoClient(mongo_uri)
db = client["cryptoskopen-eu"]
input_collection = db["in"]
output_collection = db["rw"]

# Function to fetch article details
def fetch_article_details(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
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
        soup = BeautifulSoup(html_content, 'html.parser')
        article_body = soup.find('div', class_='post-content')
        full_text = article_body.get_text(separator='\n').strip() if article_body else "Full text not found."
        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image and og_image['content'] else "https://example.com/default-image.jpg"
        return full_text, image_url
    except Exception as e:
        print(f"Error extracting article details: {e}")
        return "Full text not found.", "https://example.com/default-image.jpg"

def get_latest_article_date():
    latest_article = input_collection.find_one(sort=[("published", pymongo.DESCENDING)])
    if latest_article:
        latest_article_date = datetime.strptime(latest_article["published"], "%a, %d %b %Y %H:%M:%S %z")
        return latest_article_date.replace(tzinfo=None)  # Convert to timezone-naive datetime
    return None

def run_script(rss_feed_url, num_articles, category):
    # RSS feed URL
    feed = feedparser.parse(rss_feed_url)
    latest_article_date = get_latest_article_date()
    new_articles = []

    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6])
        if not latest_article_date or published > latest_article_date:
            new_articles.append(entry)
            if len(new_articles) >= num_articles:
                break

    count = 0
    for entry in new_articles:
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

    print(f"{count} new RSS news articles have been saved to the 'news_rewrite.in' collection in MongoDB.")

def main():
    # Hardcoded parameters for CoinTelegraph RSS feed
    rss_feed_url = 'https://cointelegraph.com/rss'
    num_articles = 10
    category = None

    # Run the script with the hardcoded parameters
    run_script(rss_feed_url, num_articles, category)

if __name__ == "__main__":
    main()