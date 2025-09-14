from fastapi import APIRouter, Depends, status, Response
from ... import security, models
from . import schemas
from .service import BookingService, get_booking_service

router = APIRouter(
    tags=["Bookings"]
)

@router.post(
    "/events/{event_id}/book", 
    response_model=schemas.BookingResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def create_booking_request(
    event_id: int, 
    booking_request: schemas.BookingCreate,
    response: Response,
    service: BookingService = Depends(get_booking_service),
    current_user: models.User = Depends(security.get_current_user)
):
    # Accept booking request and enqueue for processing
    result = service.request_booking(
        event_id=event_id,
        user=current_user,
        num_tickets=booking_request.num_tickets
    )
    # Provide a Location header for checking booking status
    response.headers["Location"] = f"/api/v1/bookings/event/{event_id}"
    return result