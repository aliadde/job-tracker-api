# app/models/applications.py 
from __future__ import annotations
import datetime
from sqlalchemy import ForeignKey, String
from app.db.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

import app.models as models 
class Applications(Base):
    __tablename__ = "applications"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    applied_at: Mapped[datetime.datetime] 
    response_date: Mapped[datetime.datetime]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    update_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    # ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # A user can have multiple companies
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))  # Status is stored in a separate table
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))  # Position is stored in a separate table
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))  # An application belongs to a specific job
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))  # A company can have multiple jobs
    resume_id:  Mapped[int] = mapped_column(ForeignKey("resumes.id"))  # An application have a specific resume
    
    # relationships
    user: Mapped["Users"] = relationship( back_populates="applications")  # type: ignore
    status: Mapped["Statuses"] = relationship( back_populates="applications")   # type: ignore
    position: Mapped["Positions"] = relationship( back_populates="applications")   # type: ignore
    job: Mapped["Jobs"] = relationship( back_populates="applications")   # type: ignore
    company: Mapped["Companies"] = relationship( back_populates="applications")   # type: ignore
    resume: Mapped["Resumes"] = relationship( back_populates="applications")   # type: ignore