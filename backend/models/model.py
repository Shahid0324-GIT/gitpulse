from sqlmodel import Field, SQLModel, func, Column, DateTime
from datetime import datetime
from typing import Optional

class GithubEvent(SQLModel, table=True):
    id: str = Field(primary_key=True)
    
    repo_name: str
    event_type: str 
    actor_name: str  
    language: Optional[str] = Field(default=None)
    is_bot: bool = Field(default=False)
    
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )