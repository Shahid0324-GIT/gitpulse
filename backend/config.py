import os

class Settings:
    PROJECT_NAME: str = "GitPulse"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    CORS_ORIGINS: list[str] = ["*"]
    REDIS_HOST: str = os.environ.get("REDIS_HOST", 'redis')
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))

settings = Settings()