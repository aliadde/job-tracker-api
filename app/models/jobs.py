import datetime

from sqlalchemy import Column, Integer, Float, String ,Boolean,TIMESTAMP, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Jobs(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    title = Column(String(255), unique=True, nullable=False)
    location = Column(String(255), nullable=False)
    employment_type = Column(String(255), nullable=False) #  Full-time / Part-time / Internship
    salary = Column(Float(10, 2), nullable=False)
    job_url  = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.datetime.now())

    # ForeignKeys
    company_id = Column(Integer, 
                        ForeignKey("companies.id", ondelete="CASCADE"),
                        nullable=False)
                        
    # relationships
    users = relationship("Users", back_populates="jobs")
    companies = relationship("Companies", back_populates="jobs") # 1 company can have many jobs    