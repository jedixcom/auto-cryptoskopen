import openai
import pymongo
from datetime import datetime, timezone, timedelta
import concurrent.futures
import os
import re
import requests
from google.cloud import storage
import nltk
from nltk.corpus import stopwords
from firebase_utils import initialize_firebase, deploy_to_firebase_hosting, final_deploy_to_firebase
from mongo_utils import connect_to_mongo
from openai_utils import generate_text, get_category, get_tags, translate_to_dutch
from html_creation import create_single_article_html
from html_update import update_category_index, update_index_html
from utils import get_current_timestamp, create_url_slug, generate_summary, remove_original_images
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

bucket_name = os.getenv('BUCKET_NAME')
base_dir = os.getenv('BASE_DIR')
google_application_credentials_base64 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
domain_name = os.getenv('DOMAIN_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
mongo_uri = os.getenv('MONGO_URI')

# Debugging environment variables
print(f"BUCKET_NAME: {bucket_name}")
print(f"BASE_DIR: {base_dir}")
print(f"GOOGLE_APPLICATION_CREDENTIALS_BASE64: {google_application_credentials_base64}")
print(f"DOMAIN_NAME: {domain_name}")
print(f"OPENAI_API_KEY: {openai_api_key}")
print(f"MONGO_URI: {mongo_uri}")

# Ensure all required environment variables are set
if not all([bucket_name, base_dir, google_application_credentials_base64, domain_name, openai_api_key, mongo_uri]):
    raise ValueError("One or more required environment variables are not set.")

google_application_credentials_path = os.path.join(base_dir, 'cryptoskopen-website', 'firebase-key.json')

# Ensure the directory for the firebase key exists
os.makedirs(os.path.dirname(google_application_credentials_path), exist_ok=True)

with open(google_application_credentials_path, 'wb') as f:
    f.write(base64.b64decode(google_application_credentials_base64))

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials_path
openai.api_key = openai_api_key

def create_directories_and_files(base_dir):
    """Create necessary directories and files if they don't exist."""
    blogx_dir = os.path.join(base_dir, 'blogx')
    index_file = os.path.join(blogx_dir, 'index.html')

    os.makedirs(blogx_dir, exist_ok=True)

    if not os.path.exists(index_file):
        with open(index_file, 'w') as file:
            file.write('<html><body><h1>Index</h1></body></html>')

def rewrite_article(article, base_dir, bucket_name, domain_name, stop_words):
    try:
        original_title = article["title"]
        original_body = article["full_text"]

        rewritten_title = generate_text(original_title, max_tokens=50)
        rewritten_title = rewritten_title[:160]

        chunk_size = 1024
        rewritten_body = ""
        for i in range(0, len(original_body), chunk_size):
            chunk = original_body[i:i + chunk_size]
            rewritten_body_chunk = generate_text(f"Rewrite in Easy to Read Business Style:\n\n{chunk}", max_tokens=chunk_size)
            rewritten_body += rewritten_body_chunk + " "

        rewritten_body = rewritten_body.strip()

        translated_title = translate_to_dutch(rewritten_title)
        translated_body = translate_to_dutch(rewritten_body)

        translated_body = remove_original_images(translated_body)

        summary = generate_summary(translated_body)

        category = get_category(translated_body)
        tags = get_tags(translated_body)

        article_data = {
            "title": translated_title,
            "link": article["link"],
            "published": article["published"],
            "summary": summary,
            "full_text": translated_body,
            "timestamp": get_current_timestamp(),
            "slug": create_url_slug(translated_title, stop_words),
            "category": category,
            "tags": tags,
            "url": f"{domain_name}/category/{category.lower()}/{create_url_slug(translated_title, stop_words)}.html"[:300]
        }

        public_url = deploy_to_firebase_hosting(article_data, base_dir, domain_name, stop_words)
        return article_data, public_url
    except Exception as e:
        print(f"Error in rewrite_article: {e}")
        return None, None

def process_article(article, base_dir, bucket_name, domain_name, stop_words, input_collection):
    try:
        article_data, public_url = rewrite_article(article, base_dir, bucket_name, domain_name, stop_words)
        if article_data:
            articles_in_category = list(input_collection.find({"category": article_data['category']}))
            update_category_index(article_data['category'], base_dir, articles_in_category, domain_name)
            return article_data, public_url
        return None, None
    except Exception as e:
        print(f"Error in process_article: {e}")
        return None, None

def cleanup():
    """Remove sensitive files after use."""
    try:
        if os.path.exists(google_application_credentials_path):
            os.remove(google_application_credentials_path)
            print("Temporary Google application credentials file removed.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def main():
    try:
        domain_name = 'https://auto-cryptoskopen-1.web.app/'
        print(f"Domain name set to: {domain_name}")

        create_directories_and_files(base_dir)
        print("Required directories and files created.")

        initialize_firebase()
        print("Firebase initialized.")

        client, db = connect_to_mongo()
        input_collection = db["in"]
        output_collection = db["rw"]
        print("Successfully connected to MongoDB")

        nltk.download('stopwords')
        stop_words = set(stopwords.words('dutch'))
        print("Stop words loaded.")

        rewritten_articles = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_article, article, base_dir, bucket_name, domain_name, stop_words, input_collection)
                for article in input_collection.find({"processed": {"$ne": True}})
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        article_data, uploaded_url = result
                        rewritten_articles.append(article_data)
                        print("\n=== Rewritten Article ===")
                        print(f"Title: {article_data['title']}")
                        print(f"Full Text: {article_data['full_text']}\n")
                        print(f"Category: {article_data['category']}\n")
                        print(f"Tags: {', '.join(article_data['tags'])}\n")
                        if uploaded_url:
                            print(f"Uploaded HTML URL: {uploaded_url}\n")
                            input_collection.update_one({"link": article_data["link"]}, {"$set": {"processed": True}})
                except Exception as e:
                    print(f"Error in processing future result: {e}")

        if rewritten_articles:
            output_collection.insert_many(rewritten_articles)
            print("Rewritten articles inserted into MongoDB")

        update_index_html(rewritten_articles, base_dir, domain_name)
        print("Index HTML updated.")

        final_deploy_to_firebase()
        print("Deployment to Firebase completed.")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    print("Starting the article rewriter script...")
    main()