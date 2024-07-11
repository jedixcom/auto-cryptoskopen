import os
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, firestore
from html_creation import create_single_article_html
from utils import create_url_slug
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


bucket_name = os.getenv('BUCKET_NAME')
base_dir = os.getenv('BASE_DIR')
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
domain_name = os.getenv('DOMAIN_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
mongo_uri = os.getenv('MONGO_URI')

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'storageBucket': bucket_name
        })
    global firestore_db
    firestore_db = firestore.client()

deploy_paths = []

def deploy_to_firebase_hosting(article_data, base_dir, domain_name, stop_words):
    local_file_path = create_single_article_html(article_data, base_dir, domain_name, stop_words)
    
    if not os.path.exists(local_file_path):
        print(f"Error: The generated HTML file was not found at {local_file_path}")
        return None

    title_slug = create_url_slug(article_data['title'], stop_words)
    category = article_data['category'].lower()
    hosting_path = f"/category/{category}/{title_slug}.html"
    
    public_dir = os.path.join(base_dir, 'category', category)
    os.makedirs(public_dir, exist_ok=True)
    destination_path = os.path.join(public_dir, f"{title_slug}.html")
    os.rename(local_file_path, destination_path)
    
    print(f"File moved to Firebase public directory at: {destination_path}")

    deploy_paths.append(destination_path)

    return f"{domain_name}/category/{category}/{title_slug}.html"

def final_deploy_to_firebase():
    if deploy_paths:
        os.system('firebase deploy')
        print("Deployed to Firebase Hosting")
    else:
        print("No files to deploy")