from sqlalchemy.orm import Session
from ... import models
from . import schemas

# Fetch a single event by ID
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

# Fetch multiple events with pagination
def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

# Create a new event
def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.model_dump(), created_by=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event