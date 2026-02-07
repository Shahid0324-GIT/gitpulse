import time
import json
import os
import redis
from datetime import datetime
from sqlmodel import Session

# Modular Imports
from database import engine, init_db
from models import GithubEvent

# Configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
QUEUE_KEY = "github_events"

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def process_event(event_json):
    try:
        data = json.loads(event_json)
        
        # Map JSON to Model
        new_event = GithubEvent(
            id=data["id"],
            repo_name=data["repo"]["name"],
            event_type=data["type"],
            actor_name=data["actor"]["login"],
            created_at=datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        )
        
        # Save to DB
        with Session(engine) as session:
            if not session.get(GithubEvent, new_event.id):
                session.add(new_event)
                session.commit()
                print(f"✅ Saved: {new_event.repo_name}", flush=True)
            else:
                print(f"⚠️ Skipped duplicate: {new_event.id}", flush=True)

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)

def main():
    print("Consumer Worker Started...", flush=True)
    time.sleep(5)
    init_db()

    while True:
        # Blocking Pop
        item = r.brpop([QUEUE_KEY], timeout=0)
        if item:
            _, event_json = item # type: ignore
            process_event(event_json)

if __name__ == "__main__":
    main()