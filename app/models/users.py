import datetime

from sqlalchemy import Column, Integer, String ,Boolean,TIMESTAMP, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_passowrd = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.datetime.now())
    
    # relationships
    companies = relationship("Companies", back_populates="users") 
    jobs = relationship("Jobs", back_populates="users")  
    
    # applications = relationship("Applications", back_populates="users") # 1 user can apply for many jobs    
