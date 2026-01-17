from database import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.sql import func


class IncidentsTable(Base):
    __tablename__ = "incidents"    
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(10), nullable=None, default="open")
    created_at = Column(DateTime, default = func.now())
    
    title = Column(String(50), nullable=False, index=True)
    description = Column(String(300), nullable=False)
    severity = Column(String(10), nullable=False)

class UserTable(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False, unique=True)
    password_hashed = Column(String(255), nullable = False)
