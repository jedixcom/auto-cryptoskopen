import feedparser
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("Missing environment variable MONGO_URI")

proxy_auth = os.getenv('PROXY_AUTH')
if not proxy_auth:
    raise EnvironmentError("Missing environment variable PROXY_AUTH")

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

# Function to fetch article details with proxy support
def fetch_article_details(link, max_retries=3, timeout=30):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    proxies = {
        'http': f'http://customer-jedixcom_wRLl9:389Hoi123OXL@us-pr.oxylabs.io:10000',
        'https': f'https://customer-jedixcom_wRLl9:389Hoi123OXL@us-pr.oxylabs.io:10000'
    }
    retries = 0
    while retries < max_retries:
        try:
            # Verify the IP address used by the proxy
            ip_check_url = 'http://httpbin.org/ip'
            print(f"Checking outgoing IP address using proxy {proxies['http']}...")
            ip_response = requests.get(ip_check_url, headers=headers, proxies=proxies, timeout=timeout)
            print(f"Outgoing IP address: {ip_response.json()}")

            print(f"Fetching article details from {link} (Attempt {retries + 1}/{max_retries}) using proxy {proxies['http']}...")
            response = requests.get(link, headers=headers, proxies=proxies, timeout=timeout)
            if response.status_code == 200:
                print(f"Successfully fetched article details from {link}.")
                full_text, image_url = extract_article_details(response.text)
                return full_text, image_url
            else:
                print(f"Failed to fetch article details from {link}. Status code: {response.status_code}")
                retries += 1
                time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.ProxyError as e:
            print(f"ProxyError while fetching {link}. Exception: {e}")
            retries += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.Timeout as e:
            print(f"Timeout while fetching {link}. Exception: {e}")
            retries += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
        except requests.exceptions.RequestException as e:
            print(f"RequestException while fetching {link}. Exception: {e}")
            retries += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
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
            except pymongo.errors.PyMongoError as e:
                print(f"Failed to save article '{entry.title}' to MongoDB. Error: {e}")

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