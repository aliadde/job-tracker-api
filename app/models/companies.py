from __future__ import annotations
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    applications: Mapped[list["Applications"]] = relationship(  # type: ignore
            back_populates="company"
    )