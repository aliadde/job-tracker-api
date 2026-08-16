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
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    applied_at: Mapped[str | None] 
    response_date: Mapped[str | None]
    created_at: Mapped[str ] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[str ] = mapped_column(default=datetime.datetime.now)

    # ForeignKeys
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))  # A user can have multiple companies
    status_id: Mapped[int | None] = mapped_column(ForeignKey("statuses.id"),nullable=True)  # Status is stored in a separate table
    position_id: Mapped[int | None] = mapped_column(ForeignKey("positions.id"),nullable=True)  # Position is stored in a separate table
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"),nullable=True)  # An application belongs to a specific job
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"),nullable=True)  # A company can have multiple jobs
    resume_id:  Mapped[int | None] = mapped_column(ForeignKey("resumes.id"),nullable=True)  # An application have a specific resume
    
    # relationships
    user: Mapped["Users"] = relationship( back_populates="applications")  # type: ignore
    status: Mapped["Statuses"] = relationship( back_populates="applications")   # type: ignore
    position: Mapped["Positions"] = relationship( back_populates="applications")   # type: ignore
    job: Mapped["Jobs"] = relationship( back_populates="applications")   # type: ignore
    company: Mapped["Companies"] = relationship( back_populates="applications")   # type: ignore
    resume: Mapped["Resumes"] = relationship( back_populates="applications")   # type: ignore