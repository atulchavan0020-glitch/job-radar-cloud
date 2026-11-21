import requests
import logging
from config import (
    GREENHOUSE_BOARDS, LEVER_BOARDS,
    ROLE_KEYWORDS, LEVEL_KEYWORDS, EXCLUDE_KEYWORDS
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def matches_criteria(title: str, location: str) -> bool:
    title_lower = title.lower()
    loc_lower = location.lower() if location else ""

    # Must not contain senior keywords
    if any(neg in title_lower for neg in EXCLUDE_KEYWORDS):
        return False

    # Must match role keyword
    has_role = any(r in title_lower for r in ROLE_KEYWORDS)
    if not has_role:
        return False

    # Must match level (intern, fresher, junior, etc.)
    has_level = any(lvl in title_lower for lvl in LEVEL_KEYWORDS)
    if not has_level:
        return False

    # Location check: Prefer Remote, India, or global
    is_location_match = any(loc in loc_lower for loc in ["india", "remote", "anywhere", "gurgaon", "noida", "delhi", "pune", "mumbai", "hyderabad", "bangalore", "bengaluru"])
    
    return is_location_match

def scan_greenhouse(company_name: str, board_token: str):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    openings = []
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            jobs = data.get("jobs", [])
            for j in jobs:
                title = j.get("title", "")
                location = j.get("location", {}).get("name", "")
                if matches_criteria(title, location):
                    openings.append({
                        "id": f"gh-{board_token}-{j.get('id')}",
                        "company": company_name,
                        "title": title,
                        "location": location,
                        "url": j.get("absolute_url"),
                        "source": "Greenhouse"
                    })
    except Exception as e:
        logging.warning(f"Error scanning Greenhouse for {company_name}: {e}")
    return openings

def scan_lever(company_name: str, site: str):
    url = f"https://api.lever.co/v0/postings/{site}?mode=json"
    openings = []
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            jobs = resp.json()
            for j in jobs:
                title = j.get("text", "")
                categories = j.get("categories", {})
                location = categories.get("location", "")
                if matches_criteria(title, location):
                    openings.append({
                        "id": f"lever-{site}-{j.get('id')}",
                        "company": company_name,
                        "title": title,
                        "location": location,
                        "url": j.get("hostedUrl"),
                        "source": "Lever"
                    })
    except Exception as e:
        logging.warning(f"Error scanning Lever for {company_name}: {e}")
    return openings

def fetch_all_openings():
    all_jobs = []
    logging.info("Scanning Greenhouse boards...")
    for gh in GREENHOUSE_BOARDS:
        found = scan_greenhouse(gh["name"], gh["token"])
        all_jobs.extend(found)

    logging.info("Scanning Lever boards...")
    for lv in LEVER_BOARDS:
        found = scan_lever(lv["name"], lv["site"])
        all_jobs.extend(found)

    logging.info(f"Total matching openings discovered: {len(all_jobs)}")
    return all_jobs
