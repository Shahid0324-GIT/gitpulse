import time
import json
import os
import redis
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, delete

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
        created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        created_at = created_at.replace(tzinfo=timezone.utc) 
        
        # 1. Clean the Data
        new_event = GithubEvent(
            id=data["id"],
            repo_name=data["repo"]["name"],
            event_type=data["type"],
            actor_name=data["actor"]["login"],
            created_at=created_at
        )
        
        # 2. Save to DB & Publish
        with Session(engine) as session:
            if not session.get(GithubEvent, new_event.id):
                session.add(new_event)
                session.commit()
                print(f"✅ Saved: {new_event.repo_name}", flush=True)
                r.publish("events_stream", new_event.model_dump_json()) 
            else:
                print(f"⚠️ Skipped duplicate: {new_event.id}", flush=True)

    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        
def cleanup_old_data():
    """Deletes events older than 24 hours to save DB space."""
    try:
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        with Session(engine) as session:
            statement = delete(GithubEvent).where(GithubEvent.created_at < cutoff_time) # type: ignore
            result = session.exec(statement)
            session.commit()
            
            if result.rowcount > 0:
                print(f"🧹 Cleanup: Deleted {result.rowcount} old events.", flush=True)
                
    except Exception as e:
        print(f"❌ Cleanup Error: {e}", flush=True)

def main():
    print("Consumer Worker Started...", flush=True)
    time.sleep(5)
    init_db()
    
    events_processed = 0

    while True:
        item = r.brpop([QUEUE_KEY], timeout=5) 
        if item:
            _, event_json = item # type: ignore
            process_event(event_json)
            
            events_processed += 1
            
            if events_processed >= 100:
                cleanup_old_data()
                events_processed = 0
                
        else:
            cleanup_old_data()

if __name__ == "__main__":
    main()