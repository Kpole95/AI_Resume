import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://example.com/page"

def get_initial_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Please make sure CLIENT_ID and CLIENT_SECRET are set in your .env file.")
        return

    auth_url = (f"https://hh.ru/oauth/authorize?response_type=code"
                f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}")
    
    print("\n--- Step 1: Authorize Your Application ---")
    print("Please visit the following URL in your browser, log in, and grant access:")
    print("\n" + auth_url + "\n")
    
    redirected_url = input("--- Step 2: Paste the full redirected URL here: ")
    
    try:
        auth_code = redirected_url.split("?code=")[1].split("&")[0]
    except IndexError:
        print("\nERROR: Could not find the authorization code in the URL you pasted.")
        return
        
    print(f"\nSuccessfully extracted authorization code...")
    
    print("\n--- Step 3: Getting Your New Tokens ---")
    
    token_url = "https://api.hh.ru/token"
    
    data = { "grant_type": "authorization_code", "client_id": CLIENT_ID,
             "client_secret": CLIENT_SECRET, "code": auth_code, "redirect_uri": REDIRECT_URI }
    
    try:
        response = requests.post(token_url, data=data, timeout=10)
        response.raise_for_status()
        new_tokens = response.json()
        
        with open(TOKEN_FILE, 'w') as f:
            json.dump(new_tokens, f, indent=4)
            
        print("\nSUCCESS! Your new tokens have been saved to config/tokens.json")
        print(f"Your new access_token starts with: {new_tokens['access_token'][:10]}...")

    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Failed to get tokens. API response: {e.response.text if e.response else str(e)}")

if __name__ == "__main__":
    get_initial_token()