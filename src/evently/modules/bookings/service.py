from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ... import models, database, queue
from ..events import repository as event_repo
from ...queue import RedisQueueClient # <-- IMPORT THE CORRECT CLASS

class BookingService:
    # Use the correct class name for the type hint
    def __init__(self, db: Session, queue_client: RedisQueueClient): # <-- FIX HERE
        self.db = db
        self.queue_client = queue_client

    def request_booking(self, event_id: int, user: models.User, num_tickets: int):
        event = event_repo.get_event(self.db, event_id)

        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # Fast-path rejection (this logic remains the same)
        if event.tickets_sold + num_tickets > event.capacity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not enough tickets available")

        # Enqueue the job for the worker to process.
        self.queue_client.enqueue_booking_request(
            user_id=user.id,
            event_id=event_id,
            num_tickets=num_tickets
        )
        
        return {"message": "Booking request received and is being processed.", "event_id": event_id}

# The dependency function needs to provide the correct class type
def get_booking_service(
    db: Session = Depends(database.get_db), 
    q_client: RedisQueueClient = Depends(queue.get_queue_client) # <-- FIX HERE
):
    return BookingService(db=db, queue_client=q_client)