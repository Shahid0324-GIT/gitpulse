import time
import requests
import json
import redis
from config import settings

# Connect to Redis
print(f"Connecting to Redis at {settings.REDIS_HOST}...", flush=True)
r = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    decode_responses=True
)

def fetch_events():
    headers = {}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    try:
        response = requests.get(settings.GITHUB_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("⚠️ Rate Limit Hit!", flush=True)
            return []
        else:
            print(f"❌ Error: {response.status_code}", flush=True)
            return []
    except Exception as e:
        print(f"❌ Network Error: {e}", flush=True)
        return []

def main():
    print("🚀 Producer Started", flush=True)
    while True:
        events = fetch_events()
        if events:
            count = 0
            for event in events:
                try:
                    r.lpush(settings.QUEUE_KEY, json.dumps(event))
                    count += 1
                except Exception as e:
                    print(f"Skipping bad event: {e}")

            print(f"✅ Pushed {count} events (All Types).", flush=True)
        
        print("Sleeping for 60s...", flush=True)
        time.sleep(60)

if __name__ == "__main__":
    main()