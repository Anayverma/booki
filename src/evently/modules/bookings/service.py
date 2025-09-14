from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ... import models, queue, database
from ..events import repository as event_repo

class BookingService:
    def __init__(self, db: Session, queue_client: queue.QueueClient):
        self.db = db
        self.queue_client = queue_client

    def request_booking(self, event_id: int, user: models.User, num_tickets: int):
        # Fetch event
        event = event_repo.get_event(self.db, event_id)

        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        # Fast-path check for ticket availability (non-locking)
        if event.tickets_sold + num_tickets > event.capacity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not enough tickets available")

        # Enqueue booking request for background processing
        self.queue_client.enqueue_booking_request(
            user_id=user.id,
            event_id=event_id,
            num_tickets=num_tickets
        )
        
        return {"message": "Booking request received and is being processed.", "event_id": event_id}

# Dependency to provide BookingService instance
def get_booking_service(
    db: Session = Depends(database.get_db), 
    q_client: queue.QueueClient = Depends(queue.get_queue_client)
):
    return BookingService(db=db, queue_client=q_client)