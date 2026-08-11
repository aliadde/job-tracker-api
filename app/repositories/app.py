from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.applications import Applications

class AppRepository:
    async def create(db: AsyncSession, ): ...