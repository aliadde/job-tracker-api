from __future__ import annotations
import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[str] = mapped_column(
        default=datetime.datetime.now
    )
    update_at: Mapped[str] = mapped_column(
        default=datetime.datetime.now
    )

    # Relationships
    applications: Mapped[list["Applications"]] = relationship( # type: ignore
        back_populates="user"
    )