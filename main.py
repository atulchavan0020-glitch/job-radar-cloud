import json
import os
import logging
from datetime import datetime
from job_scanner import fetch_all_openings
from notifier import send_job_alert_email

HISTORY_FILE = "jobs_history.json"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading {HISTORY_FILE}: {e}")
    return {"notified_ids": [], "history": []}

def save_history(data):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving {HISTORY_FILE}: {e}")

def main():
    history_data = load_history()
    seen_ids = set(history_data.get("notified_ids", []))
    
    current_jobs = fetch_all_openings()
    new_jobs = [job for job in current_jobs if job["id"] not in seen_ids]

    logging.info(f"Discovered {len(new_jobs)} genuinely new job openings.")

    if new_jobs:
        # Send Email Alert
        send_job_alert_email(new_jobs)

        # Update History
        for j in new_jobs:
            seen_ids.add(j["id"])
            j["discovered_at"] = datetime.utcnow().isoformat()
            history_data["history"].append(j)

        history_data["notified_ids"] = list(seen_ids)
        history_data["last_run"] = datetime.utcnow().isoformat()
        save_history(history_data)
    else:
        logging.info("No newly discovered openings this cycle.")

if __name__ == "__main__":
    main()
