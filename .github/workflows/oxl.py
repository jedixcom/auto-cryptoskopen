import requests
import base64
import json

# Your Oxylabs credentials
username = 'jedixcom'
password = '389Hoi123OXL'

# Oxylabs API login endpoint
login_url = "https://residential.oxylabs.io/v1/login"

# Encode credentials for Basic Auth
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# Headers for the login request
login_headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}

# Make the POST request to login and get the token
response = requests.post(login_url, headers=login_headers)

if response.status_code == 200:
    try:
        response_data = response.json()
        token = response_data.get('token')
        print(f"Received token: {token}")

        # Headers for subsequent requests using the Bearer token
        api_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Example of making a request to another endpoint using the Bearer token
        api_endpoint = "https://residential.oxylabs.io/v1/some_endpoint"  # Replace with your actual endpoint
        response = requests.get(api_endpoint, headers=api_headers)

        if response.status_code == 200:
            print("API request successful!")
            print("Response data:", response.json())
        else:
            print(f"API request failed with status code {response.status_code}")
            try:
                print("Error message:", response.json())
            except json.JSONDecodeError:
                print("Error message is not in JSON format.")
                print(response.text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print("Response content:", response.text)
else:
    print(f"Login failed with status code {response.status_code}")
    try:
        print("Error message:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Error message is not in JSON format.")
        print(response.text)