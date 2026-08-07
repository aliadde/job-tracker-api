from __future__ import annotations
from sqlalchemy import String 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Jobs(Base):   
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Relationships
    applications: Mapped[list["Applications"]] = relationship(                 # type: ignore
        back_populates="job"
    )