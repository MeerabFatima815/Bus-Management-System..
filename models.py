# ============================================================
# FILE: models.py
# TOOLS USED:
#   - SQLAlchemy : Defines database table structures as Python classes
#                  Each class = one table in PostgreSQL
# ============================================================

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id  = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email    = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


class Bus(Base):
    __tablename__ = "buses"

    bus_id     = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False)
    bus_name   = Column(String, nullable=False)
    capacity   = Column(Integer, nullable=False)
    status     = Column(String, default="Active")  # Active / Inactive

    bookings = relationship("Booking", back_populates="bus", cascade="all, delete")


class Passenger(Base):
    __tablename__ = "passengers"

    passenger_id = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    phone        = Column(String, nullable=False)
    email        = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="passenger", cascade="all, delete")


class Booking(Base):
    __tablename__ = "bookings"

    booking_id   = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.passenger_id"), nullable=False)
    bus_id       = Column(Integer, ForeignKey("buses.bus_id"), nullable=False)
    seat_number  = Column(Integer, nullable=False)
    booking_date = Column(Date, nullable=False)

    bus       = relationship("Bus", back_populates="bookings")
    passenger = relationship("Passenger", back_populates="bookings")