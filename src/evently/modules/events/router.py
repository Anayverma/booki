from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ... import database, security, models
from . import schemas, repository

router = APIRouter(
    tags=["Events"]
)

# Public endpoints
@router.get("/events", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # List events with pagination
    events = repository.get_events(db, skip=skip, limit=limit)
    return events

@router.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(database.get_db)):
    # Get single event by ID
    db_event = repository.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Admin endpoint
@router.post("/admin/events", response_model=schemas.Event, status_code=201)
def create_new_event(
    event: schemas.EventCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_admin_user)
):
    # Create a new event (admin only)
    return repository.create_event(db=db, event=event, user_id=current_user.id)