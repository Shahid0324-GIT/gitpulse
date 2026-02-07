import os

class Settings:
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))
    QUEUE_KEY: str = "github_events"
    
    GITHUB_API_URL: str = "https://api.github.com/events"
    GITHUB_TOKEN: str | None = os.environ.get("GITHUB_TOKEN")

settings = Settings()