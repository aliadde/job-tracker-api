from __future__ import annotations
import datetime
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

# from app.models import Companies, Applications
import app.models as models
class Jobs(Base):   
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    employment_type: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Full-time / Part-time / Internship
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    job_url: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )

    # Foreign Key
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    companies: Mapped[list["Companies"]] = relationship(back_populates="jobs") # type: ignore
    applications: Mapped[list["Applications"]] = relationship(                 # type: ignore
        back_populates="jobs"
    )