# ============================================================
# FILE: schemas.py
# TOOLS USED:
#   - Pydantic : Data validation library used by FastAPI
#                Defines what data the API accepts (input) and returns (output)
# ============================================================

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# ─── USER ───────────────────────────────
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    message: str
    user_id: int
    username: str

# ─── BUS ────────────────────────────────
class BusCreate(BaseModel):
    bus_number: str
    bus_name: str
    capacity: int
    status: Optional[str] = "Active"

class BusUpdate(BaseModel):
    bus_number: Optional[str] = None
    bus_name: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

class BusResponse(BaseModel):
    bus_id: int
    bus_number: str
    bus_name: str
    capacity: int
    status: str

    class Config:
        from_attributes = True

# ─── PASSENGER ──────────────────────────
class PassengerCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class PassengerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class PassengerResponse(BaseModel):
    passenger_id: int
    name: str
    phone: str
    email: str

    class Config:
        from_attributes = True

# ─── BOOKING ────────────────────────────
class BookingCreate(BaseModel):
    passenger_id: int
    bus_id: int
    seat_number: int
    booking_date: date

class BookingResponse(BaseModel):
    booking_id: int
    passenger_id: int
    bus_id: int
    seat_number: int
    booking_date: date

    class Config:
        from_attributes = True

# ─── DASHBOARD ──────────────────────────
class DashboardStats(BaseModel):
    total_buses: int
    total_passengers: int
    total_bookings: int
    active_buses: int