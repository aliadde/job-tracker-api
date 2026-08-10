from sqlalchemy.ext.asyncio import AsyncSession


class PositionRepository:
    async def create(self, db: AsyncSession, position: str):
        from app.models.positions import Positions

        position = Positions(position=position)

        db.add(position)
        await db.commit()
        await db.refresh(position)
        return position