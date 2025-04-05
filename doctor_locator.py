from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from geopy.distance import geodesic
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = "mysql+pymysql://user:password@localhost/healthcare"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI instance
app = FastAPI()

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

# Doctor & Facility Model
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Dependency for DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication function
def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# API: Get all doctors
@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

# API: Find nearby doctors based on location
@app.get("/doctors/nearby")
def get_nearby_doctors(lat: float, lon: float, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    nearby_doctors = [doctor for doctor in doctors if geodesic((lat, lon), (doctor.latitude, doctor.longitude)).km < 10]
    return nearby_doctors

# API: Filter by specialty
@app.get("/doctors/filter")
def filter_doctors(specialty: str, db: Session = Depends(get_db)):
    return db.query(Doctor).filter(Doctor.specialty == specialty).all()

# API: Add a doctor (Admin only)
@app.post("/doctors")
def add_doctor(name: str, specialty: str, lat: float, lon: float, contact: str, token: str, db: Session = Depends(get_db)):
    user = authenticate_user(token)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_doctor = Doctor(name=name, specialty=specialty, latitude=lat, longitude=lon, contact=contact)
    db.add(new_doctor)
    db.commit()
    return {"message": "Doctor added successfully"}
