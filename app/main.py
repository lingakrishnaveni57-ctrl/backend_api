from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Assignment API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API Running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
