import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# This path is still used for local development
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"

def get_current_access_token():
    """
    This is the main function the application will call.
    It checks if the current token is valid. If not, it gets a new one.
    """
    # First, try to get tokens from environment variables (for Render deployment)
    access_token = os.getenv("ACCESS_TOKEN")
    
    # If in deployment and token is valid, use it
    if access_token and validate_token(access_token):
        print("INFO: Using valid access token from environment.")
        return access_token
        
    # If in deployment and token is invalid, refresh it
    elif os.getenv("CLIENT_ID"):
        print("INFO: Deployed access token is invalid or missing. Refreshing...")
        return refresh_token()

    # --- Fallback for Local Development ---
    else:
        print("INFO: Running locally. Checking local tokens.json...")
        try:
            with open(TOKEN_FILE, 'r') as f:
                local_tokens = json.load(f)
            local_access_token = local_tokens.get("access_token")

            if local_access_token and validate_token(local_access_token):
                print("INFO: Local token is valid.")
                return local_access_token
            else:
                print("INFO: Local token is invalid or expired. Refreshing...")
                return refresh_token()
        except (FileNotFoundError, json.JSONDecodeError):
            print("INFO: tokens.json not found or empty. Refreshing for the first time...")
            return refresh_token()


def validate_token(token):
    """Validates a token by making a lightweight API call."""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://api.hh.ru/me', headers=headers, timeout=15)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def refresh_token():
    """Refreshes the hh.ru API token using the best available credentials."""
    # Prioritize environment variables for deployment
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token_val = os.getenv("REFRESH_TOKEN")

    # If not in deployment, use local .env file
    if not client_id:
        print("INFO: Loading credentials from local .env file.")
        load_dotenv(BASE_DIR / ".env")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        try:
            with open(TOKEN_FILE, 'r') as f:
                refresh_token_val = json.load(f).get("refresh_token")
        except (FileNotFoundError, json.JSONDecodeError):
            refresh_token_val = None

    if not client_id or not client_secret:
        raise ValueError("FATAL: CLIENT_ID or CLIENT_SECRET not found.")

    # Decide whether to get a new token or refresh an old one
    grant_type = 'refresh_token' if refresh_token_val else 'client_credentials'
    data = {'grant_type': grant_type}
    if grant_type == 'refresh_token':
        data['refresh_token'] = refresh_token_val
    
    try:
        print(f"INFO: Requesting new token from hh.ru with grant_type: {grant_type}...")
        response = requests.post(
            'https://api.hh.ru/token',
            data=data,
            auth=(CLIENT_ID, CLIENT_SECRET), # Auth works for both grant types
            timeout=15
        )
        response.raise_for_status()
        new_tokens = response.json()
        new_access_token = new_tokens.get("access_token")
        print("INFO: New access token received successfully.")

        # If running locally, save the new tokens
        if not os.getenv("RENDER"): # RENDER automatically sets this env var
            with open(TOKEN_FILE, 'w') as f:
                json.dump(new_tokens, f, indent=4)
            print("INFO: Updated local tokens.json")
            
        return new_access_token
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not refresh token. Reason: {e}")
        raise Exception("Failed to get a new token from hh.ru.")