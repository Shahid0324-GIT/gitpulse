from sqlmodel import Field, SQLModel, func, Column, DateTime
from datetime import datetime

# This Class represents our Table in the Database
class GithubEvent(SQLModel, table=True):
    id: str = Field(primary_key=True)
    
    # The data we want to save
    repo_name: str
    event_type: str  # e.g., "PushEvent", "WatchEvent"
    actor_name: str  # Who did it?
    
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )