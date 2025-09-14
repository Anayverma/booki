from pydantic import BaseModel
from datetime import datetime

# Base schema for event
class EventBase(BaseModel):
    name: str
    venue: str
    description: str | None = None
    start_time: datetime
    capacity: int

# Schema for creating an event
class EventCreate(EventBase):
    pass

# Schema returned for event info
class Event(EventBase):
    id: int
    tickets_sold: int
    created_by: int
    
    class Config:
        from_attributes = True  # Allow ORM objects