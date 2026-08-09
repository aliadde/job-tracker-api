# app/models/statuses.py 
from __future__ import annotations
from sqlalchemy import  String
from app.db.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Statuses(Base):
    __tablename__ = "statuses"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    # relationships
    applications: Mapped[list["Applications"]] = relationship( back_populates="status")  # type: ignore