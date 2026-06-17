# ============================================================
# FILE: main.py
# TOOLS USED:
#   - FastAPI        : Python web framework for building APIs
#   - Uvicorn        : ASGI server to run FastAPI
#   - CORS Middleware: Allows frontend to talk to backend
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from database import SessionLocal, engine, Base
from models import User, Bus, Passenger, Booking
from schemas import (
    UserCreate, UserLogin, UserResponse,
    BusCreate, BusUpdate, BusResponse,
    PassengerCreate, PassengerUpdate, PassengerResponse,
    BookingCreate, BookingResponse,
    DashboardStats, LoginResponse
)
import auth

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bus Management System API", version="1.0.0")

# Allow frontend (HTML/JS) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency: get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Bus Management System API is running!"}

# ─────────────────────────────────────────
# API 1: REGISTER USER
# ─────────────────────────────────────────
@app.post("/register", response_model=UserResponse, tags=["Authentication"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ─────────────────────────────────────────
# API 2: LOGIN USER
# ─────────────────────────────────────────
@app.post("/login", response_model=LoginResponse, tags=["Authentication"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user_id": db_user.user_id, "username": db_user.username}

# ─────────────────────────────────────────
# API 3: ADD BUS
# ─────────────────────────────────────────
@app.post("/buses", response_model=BusResponse, tags=["Bus Management"])
def add_bus(bus: BusCreate, db: Session = Depends(get_db)):
    existing = db.query(Bus).filter(Bus.bus_number == bus.bus_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bus number already exists")
    new_bus = Bus(**bus.dict())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus

# ─────────────────────────────────────────
# API 4: GET ALL BUSES
# ─────────────────────────────────────────
@app.get("/buses", response_model=List[BusResponse], tags=["Bus Management"])
def get_all_buses(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Bus)
    if search:
        query = query.filter(
            Bus.bus_name.ilike(f"%{search}%") | Bus.bus_number.ilike(f"%{search}%")
        )
    return query.all()

# ─────────────────────────────────────────
# API 5: GET SINGLE BUS
# ─────────────────────────────────────────
@app.get("/buses/{bus_id}", response_model=BusResponse, tags=["Bus Management"])
def get_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

# ─────────────────────────────────────────
# API 6: UPDATE BUS
# ─────────────────────────────────────────
@app.put("/buses/{bus_id}", response_model=BusResponse, tags=["Bus Management"])
def update_bus(bus_id: int, bus_data: BusUpdate, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    for key, value in bus_data.dict(exclude_unset=True).items():
        setattr(bus, key, value)
    db.commit()
    db.refresh(bus)
    return bus

# ─────────────────────────────────────────
# API 7: DELETE BUS
# ─────────────────────────────────────────
@app.delete("/buses/{bus_id}", tags=["Bus Management"])
def delete_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.bus_id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    db.delete(bus)
    db.commit()
    return {"message": f"Bus {bus_id} deleted successfully"}

# ─────────────────────────────────────────
# API 8: ADD PASSENGER
# ─────────────────────────────────────────
@app.post("/passengers", response_model=PassengerResponse, tags=["Passenger Management"])
def add_passenger(passenger: PassengerCreate, db: Session = Depends(get_db)):
    new_passenger = Passenger(**passenger.dict())
    db.add(new_passenger)
    db.commit()
    db.refresh(new_passenger)
    return new_passenger

# ─────────────────────────────────────────
# API 9: GET ALL PASSENGERS
# ─────────────────────────────────────────
@app.get("/passengers", response_model=List[PassengerResponse], tags=["Passenger Management"])
def get_all_passengers(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Passenger)
    if search:
        query = query.filter(
            Passenger.name.ilike(f"%{search}%") | Passenger.email.ilike(f"%{search}%")
        )
    return query.all()

# ─────────────────────────────────────────
# API 10: GET SINGLE PASSENGER
# ─────────────────────────────────────────
@app.get("/passengers/{passenger_id}", response_model=PassengerResponse, tags=["Passenger Management"])
def get_passenger(passenger_id: int, db: Session = Depends(get_db)):
    passenger = db.query(Passenger).filter(Passenger.passenger_id == passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return passenger

# ─────────────────────────────────────────
# API 11: UPDATE PASSENGER
# ─────────────────────────────────────────
@app.put("/passengers/{passenger_id}", response_model=PassengerResponse, tags=["Passenger Management"])
def update_passenger(passenger_id: int, data: PassengerUpdate, db: Session = Depends(get_db)):
    passenger = db.query(Passenger).filter(Passenger.passenger_id == passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(passenger, key, value)
    db.commit()
    db.refresh(passenger)
    return passenger

# ─────────────────────────────────────────
# API 12: DELETE PASSENGER
# ─────────────────────────────────────────
@app.delete("/passengers/{passenger_id}", tags=["Passenger Management"])
def delete_passenger(passenger_id: int, db: Session = Depends(get_db)):
    passenger = db.query(Passenger).filter(Passenger.passenger_id == passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    db.delete(passenger)
    db.commit()
    return {"message": f"Passenger {passenger_id} deleted successfully"}

# ─────────────────────────────────────────
# API 13: BOOK TICKET
# ─────────────────────────────────────────
@app.post("/bookings", response_model=BookingResponse, tags=["Booking Management"])
def book_ticket(booking: BookingCreate, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.bus_id == booking.bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    passenger = db.query(Passenger).filter(Passenger.passenger_id == booking.passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    new_booking = Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# ─────────────────────────────────────────
# API 14: GET ALL BOOKINGS
# ─────────────────────────────────────────
@app.get("/bookings", response_model=List[BookingResponse], tags=["Booking Management"])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

# ─────────────────────────────────────────
# API 15: CANCEL BOOKING
# ─────────────────────────────────────────
@app.delete("/bookings/{booking_id}", tags=["Booking Management"])
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": f"Booking {booking_id} cancelled successfully"}

# ─────────────────────────────────────────
# API 16: DASHBOARD STATS
# ─────────────────────────────────────────
@app.get("/dashboard", response_model=DashboardStats, tags=["Dashboard"])
def get_dashboard(db: Session = Depends(get_db)):
    total_buses = db.query(Bus).count()
    total_passengers = db.query(Passenger).count()
    total_bookings = db.query(Booking).count()
    active_buses = db.query(Bus).filter(Bus.status == "Active").count()
    return {
        "total_buses": total_buses,
        "total_passengers": total_passengers,
        "total_bookings": total_bookings,
        "active_buses": active_buses
    }