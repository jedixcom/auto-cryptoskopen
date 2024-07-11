import feedparser
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import os

def display_menu():
    print("---------------------------------------------------")
    print("Welcome to DutchJinn News-Manipulator - IN MDB 1.0")
    print("---------------------------------------------------")
    print("Menu:\n")
    print("1. Set RSS")
    print("2. Set No. Articles")
    print("3. Select Category")
    print("4. CoinTelegraph RSS")
    print("5. Run Script")
    print("6. Clear MongoDB - Collection: news_rewrite.news_rewrite.in")
    print("7. Clear MongoDB - Collection: news_rewrite.saved_rewritten")
    print("8. Exit")

def get_user_choice():
    choice = input("Enter your choice (1-8): ")
    return choice

def set_rss():
    rss_url = input("Enter RSS feed URL: ")
    return rss_url

def set_number_of_articles():
    try:
        num_articles = int(input("Enter the number of articles to process: "))
        return num_articles
    except ValueError:
        print("Invalid number. Please enter a valid integer.")
        return None

def select_category():
    category = input("Enter the category to filter articles: ")
    return category

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

def run_script(rss_feed_url, num_articles, category):
    # RSS feed URL
    feed = feedparser.parse(rss_feed_url)

    # Save articles to MongoDB with retry logic
    count = 0
    for entry in feed.entries:
        if count >= num_articles:
            break

        # Check if the article already exists
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

def clear_collection(collection):
    try:
        collection.delete_many({})
        print(f"Collection {collection.name} cleared.")
    except pymongo.errors.PyMongoError as e:
        print(f"Failed to clear collection {collection.name}. Error: {e}")

def main():
    rss_feed_url = None
    num_articles = None
    category = None

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            rss_feed_url = set_rss()
        elif choice == '2':
            num_articles = set_number_of_articles()
        elif choice == '3':
            category = select_category()
        elif choice == '4':
            rss_feed_url = 'https://cointelegraph.com/rss'
            num_articles = 25
            category = None
            print("CoinTelegraph RSS feed URL set to process 5 articles with no specific category.")
        elif choice == '5':
            if rss_feed_url and num_articles:
                run_script(rss_feed_url, num_articles, category)
            else:
                print("Please set RSS feed URL and number of articles before running the script.")
        elif choice == '6':
            clear_collection(input_collection)
        elif choice == '7':
            clear_collection(output_collection)
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()