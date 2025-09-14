from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# User table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # user/admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")
    events_created = relationship("Event", back_populates="creator")

# Event table
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    venue = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    tickets_sold = Column(Integer, default=0, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship("User", back_populates="events_created")
    bookings = relationship("Booking", back_populates="event")
    
    __table_args__ = (
        CheckConstraint('tickets_sold <= capacity', name='check_tickets_sold_le_capacity'),
        CheckConstraint('tickets_sold >= 0', name='check_tickets_sold_ge_0'),
    )

# Booking table
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    num_tickets = Column(Integer, nullable=False)
    status = Column(String, default="CONFIRMED", nullable=False)  # CONFIRMED/CANCELLED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")