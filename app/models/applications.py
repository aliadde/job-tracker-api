# app/models/applications.py 
from __future__ import annotations
import datetime
from sqlalchemy import ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

import app.models as models 
class Applications(Base):
    __tablename__ = "applications"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    status: Mapped[bool] = mapped_column(nullable=False)
    applied_at: Mapped[datetime.datetime] 
    response_date: Mapped[datetime.datetime]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    update_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    # ForeignKeys
    user_id: Mapped[int] =mapped_column( ForeignKey("users.id")) # user can have multiple Company
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))  # a application can hvae multiple Company

    # relationships
    user: Mapped["Users"] = relationship( back_populates="applications")  # type: ignore
    jobs: Mapped[list["Jobs"]] = relationship( back_populates="applications")   # type: ignore