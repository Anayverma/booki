import redis
import json
from .config import settings

class RedisQueueClient:
    def __init__(self, url):
        # Connect to the Redis instance
        self.redis_client = redis.from_url(url)
        # We'll use a Redis List as our simple queue
        self.queue_name = "booking_queue"

    def enqueue_booking_request(self, user_id: int, event_id: int, num_tickets: int):
        job_payload = {
            "user_id": user_id,
            "event_id": event_id,
            "num_tickets": num_tickets
        }
        job_json = json.dumps(job_payload)
        
        # 'rpush' adds the job to the right side (end) of the list
        self.redis_client.rpush(self.queue_name, job_json)
        
        print(f"ENQUEUED JOB TO REDIS: {job_json}")
        return True

# Create a single, shared instance of the client
queue_client = RedisQueueClient(url=settings.REDIS_URL)

def get_queue_client():
    return queue_client