import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from backend.database.db_session import get_db
from backend.database.db_models import Job
from backend.job_fetching.init_tokens import get_credentials, validate_token, refresh_token

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "jobs.json"

def fetch_jobs():
    # Get credentials and validate token
    creds = get_credentials()
    access_token = creds.get("access_token")

    if not access_token or not validate_token(access_token):
        print("[INFO] Token invalid or missing. Refreshing...")
        access_token = refresh_token()
        if not access_token:
            print("[ERROR] Failed to refresh token.")
            return 0

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.hh.ru/vacancies"
    params = {
        "per_page": 100,
        "area": 1,  # Moscow
        "text": "developer"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[ERROR] HH.ru API responded with {response.status_code}: {response.text}")
        return 0

    jobs = []
    db = next(get_db())
    data = response.json()

    for item in data.get("items", []):
        job_data = {
            "id": item["id"],
            "title": item["name"],
            "description": item.get("description", ""),
            "requirements": item.get("snippet", {}).get("requirement", ""),
            "language": "ru" if "ru" in item.get("name", "").lower() else "en"
        }
        jobs.append(job_data)

        # Save to MySQL
        job = Job(
            id=int(item["id"]),
            title=item["name"],
            url=item.get("alternate_url", ""),
            description=item.get("description", ""),
            requirements={"snippet": item.get("snippet", {}).get("requirement", "")},
            language=job_data["language"]
        )
        db.merge(job)  # merge to avoid duplicate PK errors
    db.commit()

    # Save to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)

    print(f"[INFO] Fetched and saved {len(jobs)} jobs")
    return len(jobs)

if __name__ == "__main__":
    fetch_jobs()
