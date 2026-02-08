from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, desc
import redis.asyncio as redis 
import asyncio

from config import settings
from database.db import init_db, get_session
from models.model import GithubEvent
from schemas import EventResponse

# --- LIFECYCLE ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Initializing...")
    init_db()
    yield
    print("Shutdown: cleanup...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ASYNC REDIS CONNECTION ---
redis_client = redis.from_url(f"redis://{settings.REDIS_HOST}:6379", decode_responses=True)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/events/", response_model=list[EventResponse])
def read_events(
    session: Session = Depends(get_session), 
    limit: int = 50, 
    offset: int = 0  
):
    statement = select(GithubEvent).order_by(desc(GithubEvent.created_at)).offset(offset).limit(limit)
    events = session.exec(statement).all()
    return events

# --- WEBSOCKET ENDPOINT ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("events_stream")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            
            if message and message["type"] == "message":
                await websocket.send_text(message["data"])
            
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await pubsub.close()
        
