from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EventResponse(BaseModel):
    id: str
    repo_name: str
    event_type: str
    actor_name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)