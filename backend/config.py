import os

class Settings:
    PROJECT_NAME: str = "GitPulse"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()