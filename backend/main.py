from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, desc

# Modular Imports
from config import settings
from database.db import init_db, get_session
from models.model import GithubEvent
from schemas import EventResponse  # <--- Using the new Schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Initializing Database Tables...")
    init_db()
    yield
    print("Shutdown: Cleaning up...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "backend"}

# The 'response_model' parameter automatically filters data using your Schema
@app.get("/events/", response_model=list[EventResponse], tags=["Events"])
def read_events(
    session: Session = Depends(get_session), 
    limit: int = 100
):
    """Fetch latest events"""
    statement = select(GithubEvent).order_by(desc(GithubEvent.created_at)).limit(limit)
    events = session.exec(statement).all()
    return events