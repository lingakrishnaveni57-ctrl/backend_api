from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)   # <-- add this
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    otp = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

