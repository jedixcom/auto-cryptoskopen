import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

bucket_name = os.getenv('BUCKET_NAME')
base_dir = os.getenv('BASE_DIR')
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
domain_name = os.getenv('DOMAIN_NAME', 'https://auto-cryptoskopen-1.web.app/')
openai_api_key = os.getenv('OPENAI_API_KEY')
mongo_uri = os.getenv('MONGO_URI')