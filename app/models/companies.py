import datetime

from sqlalchemy import Column, Integer, String ,Boolean,TIMESTAMP, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Companies(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(255), unique=True, nullable=False)
    location = Column(String(255), nullable=False)
    employment_type = Column(String(255), nullable=False) #  Full-time / Part-time / Internship
    salary = Column(Boolean, default=True)
    job_url  = Column(String(255))
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.datetime.now())

    # ForeignKeys
    user_id = Column(Integer, ForeignKey("users.id")) # user can have multiple Company

    # relationships
    users = relationship("Users", back_populates="companies")
    jobs = relationship("Jobs", back_populates="companies")
    