import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import UserSignup, UserVerify, UserLogin
from .auth import hash_password, verify_password, create_access_token, get_current_user
from .email_utils import send_otp_email

router = APIRouter()

@router.post("/signup", summary="Signup with email", description="Registers a new user and sends OTP to email.")
def signup(data: UserSignup, db: Session = Depends(get_db)):
    otp = str(random.randint(100000, 999999))
    user = User(email=data.email, password=hash_password(data.password), otp=otp, is_verified=False)
    db.add(user)
    db.commit()
    send_otp_email(data.email, otp)
    return {"message": "OTP sent to your email"}

@router.post("/verify-otp", summary="Verify OTP", description="Verifies OTP and activates account.")
def verify(data: UserVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.otp != data.otp:
        return {"error": "Invalid OTP"}
    user.is_verified = True
    user.otp = None
    db.commit()
    return {"message": "Account verified"}

@router.post("/login", summary="Login", description="Logs in verified user and returns JWT.")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password) or not user.is_verified:
        return {"error": "Invalid credentials or account not verified"}
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", summary="Profile page", description="Returns user profile. Requires JWT.")
def profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "verified": current_user.is_verified}

