import time
import json
import redis
from sqlalchemy.orm import Session
from evently.database import SessionLocal
from evently import models
from evently.config import settings

def process_booking_job(job_payload: dict):
    """
    This function contains the transactional logic to safely book a ticket.
    This version includes more explicit commits and detailed logging for debugging.
    """
    db: Session = SessionLocal()
    
    user_id = job_payload['user_id']
    event_id = job_payload['event_id']
    num_tickets = job_payload['num_tickets']

    print(f"--- [WORKER] Processing job for User {user_id} on Event {event_id} for {num_tickets} tickets ---")
    
    try:
        # Start a transaction
        db.begin()
        
        # =================== THE CRITICAL SECTION ===================
        # Lock the specific event row for the duration of this transaction.
        event = db.query(models.Event).filter(models.Event.id == event_id).with_for_update().first()
        # ==========================================================

        if not event:
            print(f"[WORKER] ERROR: Event {event_id} not found. Rolling back.")
            db.rollback()
            return

        print(f"[WORKER] DB STATE: Event '{event.name}' has {event.tickets_sold}/{event.capacity} tickets sold before update.")

        if (event.tickets_sold + num_tickets) <= event.capacity:
            event.tickets_sold += num_tickets
            
            new_booking = models.Booking(
                user_id=user_id,
                event_id=event_id,
                num_tickets=num_tickets,
                status='CONFIRMED'
            )
            db.add(new_booking)
            
            print(f"[WORKER] LOGIC: Success. Preparing to commit. New count will be: {event.tickets_sold}/{event.capacity}")
            
            db.commit()
            
            print(f"[WORKER] COMMIT SUCCESSFUL: Booking confirmed and ticket count updated in DB.")
        else:
            print(f"[WORKER] LOGIC: Failure. Not enough tickets available. Rolling back.")
            db.rollback()
    
    except Exception as e:
        print(f"[WORKER] UNEXPECTED ERROR: {e}. Rolling back transaction.")
        db.rollback()
    finally:
        # Always close the session to release the connection.
        db.close()
        print(f"--- [WORKER] Job processing finished. Session closed. ---")


def main_worker_loop():
    """
    This is the main loop that connects to Redis and waits for jobs.
    """
    print("--- Booking Worker Service Started (Redis Mode) ---")
    redis_client = redis.from_url(settings.REDIS_URL)
    queue_name = "booking_queue"
    
    print("--- Waiting for booking jobs from Redis... ---")
    while True:
        try:
            # Block and wait for a job from the 'booking_queue' list in Redis
            _, job_json = redis_client.blpop(queue_name, timeout=0)
            
            if job_json:
                decoded_job = job_json.decode('utf-8')
                print(f"[WORKER] Received job from Redis: {decoded_job}")
                
                job_payload = json.loads(decoded_job)
                process_booking_job(job_payload)
            
        except Exception as e:
            print(f"[WORKER] Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main_worker_loop()