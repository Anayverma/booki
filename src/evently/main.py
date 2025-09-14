from fastapi import FastAPI
from .database import engine, Base
from .modules.auth import router as auth_router
from .modules.events import router as events_router
from .modules.bookings import router as bookings_router

# Create all database tables on startup (for development)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Evently API",
    description="Backend system for an event ticketing platform.",
    version="1.0.0"
)

# Health check endpoint
@app.get("/")
def read_root():
    return {"status": "ok"}

# Include routers
api_v1_prefix = "/api/v1"
app.include_router(auth_router.router, prefix=api_v1_prefix)
app.include_router(events_router.router, prefix=api_v1_prefix)
app.include_router(bookings_router.router, prefix=api_v1_prefix)