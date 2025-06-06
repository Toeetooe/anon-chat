from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)        # anonymous visible name
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    real_username = Column(String)               # for admin tracking

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

