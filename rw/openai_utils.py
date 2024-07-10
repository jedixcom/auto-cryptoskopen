#openai_utils.py
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_text(prompt, max_tokens=2000):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rewrite in Business Style."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.8
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return prompt

def get_category(full_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Classify the category of the following text with one word."},
                {"role": "user", "content": full_text}
            ],
            max_tokens=10
        )
        return response.choices[0].message["content"].strip().split()[0]
    except Exception as e:
        print(f"Error getting category: {e}")
        return "Uncategorized"

def get_tags(full_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate 1 tag for the following text. Keep them short — between 1 and 3 words."},
                {"role": "user", "content": full_text}
            ],
            max_tokens=20
        )
        return response.choices[0].message["content"].strip().split(", ")[:3]
    except Exception as e:
        print(f"Error getting tags: {e}")
        return ["Tag1", "Tag2", "Tag3"]

def translate_to_dutch(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following text to Dutch."},
                {"role": "user", "content": text}
            ],
            max_tokens=2000,
            temperature=0.8
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return text