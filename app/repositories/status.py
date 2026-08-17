from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.statuses import Statuses


class StatusRepository:
    async def create(self, db: AsyncSession, status: str):
        from app.models.statuses import Statuses
        status = Statuses(status=status)

        db.add(status)
        await db.commit()
        await db.refresh(status)
        return status
    
    async def get_all(self, db:AsyncSession) -> list[Statuses]:
        from app.models.statuses import Statuses
        stmt = select(Statuses)
        result = await db.execute(stmt)
        result = result.scalars().all()
        return result