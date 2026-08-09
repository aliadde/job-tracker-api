from sqlalchemy.ext.asyncio import AsyncSession


class StatusRepository:
    async def create(self, db: AsyncSession, status: str):
        from app.models.statuses import Statuses

        status = Statuses(status=status)

        db.add(status)
        await db.commit()
        await db.refresh(status)
        return status