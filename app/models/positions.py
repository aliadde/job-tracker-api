# app/models/resumes.py 
from __future__ import annotations
from sqlalchemy import  String
from app.db.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Positions(Base):
    __tablename__ = "positions"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    position: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    
    # relationships
    applications: Mapped[list["Applications"]] = relationship( back_populates="position")  # type: ignore