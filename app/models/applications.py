import datetime
from sqlalchemy import Column, Integer, String ,Boolean,TIMESTAMP, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    status = Column(Boolean, nullable=False)
    applied_at = Column(TIMESTAMP)
    response_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    update_at = Column(TIMESTAMP, default=datetime.datetime.now())

    # ForeignKeys
    user_id = Column(Integer, ForeignKey("users.id")) # user can have multiple Company
    job_id = Column(Integer, ForeignKey("jobs.id"))  # a application can hvae multiple Company

    # relationships
    users = relationship("Users", back_populates="applications")
    jobs = relationship("Jobs", back_populates="applications")