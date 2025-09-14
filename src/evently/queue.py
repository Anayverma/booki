import json

class QueueClient:
    def enqueue_booking_request(self, user_id: int, event_id: int, num_tickets: int):
        # Simulate sending a booking job to a queue
        job_payload = {
            "user_id": user_id,
            "event_id": event_id,
            "num_tickets": num_tickets
        }
        print(f"ENQUEUED BOOKING JOB: {json.dumps(job_payload)}")
        return True  # In real use, this would be async

# Singleton instance (could be extended for concurrency in real setup)
queue_client = QueueClient()

def get_queue_client():  # Dependency helper
    return queue_client