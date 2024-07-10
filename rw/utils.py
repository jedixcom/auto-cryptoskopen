import os
import re
import nltk
from nltk.corpus import stopwords

def get_user_input():
    domain_name = input("Enter domain name (e.g., headlinesmagazine.com): ").strip()
    if not domain_name.startswith("http://") and not domain_name.startswith("https://"):
        domain_name = "https://" + domain_name
    return domain_name

def get_current_timestamp():
    from datetime import datetime, timezone, timedelta
    amsterdam_tz = timezone(timedelta(hours=2))
    return datetime.now(amsterdam_tz).strftime('%Y-%m-%d %H:%M:%S')

def create_url_slug(title, stop_words):
    title = title.replace("'", "")
    words = [word for word in title.split() if word.lower() not in stop_words and not word.isdigit()]
    important_words = words[:5]
    slug = '-'.join(important_words)
    slug = re.sub(r'[^a-zA-Z0-9-]', ' ', slug).strip()
    slug = re.sub(r'\s+', '-', slug)
    if slug.endswith('.'):
        slug = slug[:-1]
    return slug.lower()

def generate_summary(full_text, char_limit=320):
    if len(full_text) <= char_limit:
        return full_text
    else:
        summary = full_text[:char_limit]
        if summary.endswith(' ') and full_text[char_limit:]:
            return summary.rstrip() + '...'
        else:
            return summary.rsplit(' ', 1)[0] + '...'

def remove_original_images(html_content):
    return re.sub(r'<img[^>]*src="https://images\.cointelegraph\.com/[^>]*>', '', html_content)

def download_stopwords():
    nltk.download('stopwords')
    return set(stopwords.words('dutch'))