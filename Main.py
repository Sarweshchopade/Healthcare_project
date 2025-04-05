from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import User
from app.routes import auth, symptom_checker, doctor_locator, medicine_availability

# Initialize FastAPI app
app = FastAPI()

# Database setup
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(symptom_checker.router, prefix="/symptoms", tags=["Symptom Checker"])
app.include_router(doctor_locator.router, prefix="/doctors", tags=["Doctor Locator"])
app.include_router(medicine_availability.router, prefix="/medicines", tags=["Medicine Availability"])

@app.get("/")
def home():
    return {"message": "Welcome to Healthcare Assistant API"}
