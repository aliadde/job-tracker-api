from __future__ import annotations
import datetime
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

# from app.models import Users, Jobs
import app.models as models
class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    employment_type: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Full-time / Part-time / Internship
    salary: Mapped[bool] = mapped_column(Boolean, default=True)
    job_url: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationships
    user: Mapped[list["Users"]] = relationship(back_populates="companies") # type: ignore 
    jobs: Mapped[list["Jobs"]] = relationship(back_populates="companies")  # type: ignore