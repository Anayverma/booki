from pydantic import BaseModel, Field

# Schema for booking request
class BookingCreate(BaseModel):
    num_tickets: int = Field(..., gt=0)  # Must book at least 1 ticket

# Schema for booking info
class Booking(BaseModel):
    id: int
    event_id: int
    user_id: int
    num_tickets: int
    status: str
    
    class Config:
        from_attributes = True  # Allow ORM objects

# Schema for booking response
class BookingResponse(BaseModel):
    message: str
    event_id: int