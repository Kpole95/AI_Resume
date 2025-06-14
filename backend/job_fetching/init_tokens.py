import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

IS_STREAMLIT = os.getenv("RUNNING_STREAMLIT", "false").lower() == "true"


# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"


def get_credentials():
    """Gets credentials from .env + tokens.json."""
    load_dotenv(BASE_DIR / ".env")
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Token file not found at {TOKEN_FILE}")
    with open(TOKEN_FILE, 'r') as f:
        tokens = json.load(f)
    return {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token")
    }



def validate_token(access_token: str) -> bool:
    """Check if current access token is still valid."""
    url = "https://api.hh.ru/vacancies?per_page=1"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def refresh_token():
    """Refresh hh.ru API token and save it to file (local only)."""
    creds = get_credentials()
    if not creds.get("refresh_token"):
        raise ValueError("No refresh token provided.")

    print("Refreshing access token from hh.ru...")
    url = "https://api.hh.ru/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh_token"],
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"]
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to refresh token: {e}")

    new_tokens = response.json()
    access_token = new_tokens["access_token"]

    # Save locally only
    if not IS_STREAMLIT:
        with open(TOKEN_FILE, 'w') as f:
            json.dump(new_tokens, f, indent=4)
        print("Access token refreshed and saved to tokens.json.")
    
    return access_token
