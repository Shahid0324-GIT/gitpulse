from sqlmodel import create_engine, Session, SQLModel
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

def init_db():
    """Create tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI Routes"""
    with Session(engine) as session:
        yield session