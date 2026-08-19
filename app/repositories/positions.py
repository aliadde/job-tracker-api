from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class PositionRepository:
    async def create(self, db: AsyncSession, position: str):
        from app.models.positions import Positions

        position = Positions(position=position)

        db.add(position)
        await db.commit()
        await db.refresh(position)
        return position
    
    async def get_by_name(self, db:AsyncSession, name: str):
        from app.models.positions import Positions
        stmt = select(Positions).where(Positions.position == name)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    async def get_all(self, db:AsyncSession):
        from app.models.positions import Positions
        stmt = select(Positions)
        result = await db.execute(stmt)
        return result.scalars().all()
