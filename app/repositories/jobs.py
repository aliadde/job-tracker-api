from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.jobs import Jobs


class JobRepository:
    
    async def create(self, db: AsyncSession, title: str):
        job = Jobs(title=title)

        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job
    
    async def get_by_job_title(self, db: AsyncSession, title: str)-> Jobs|None:
        stmt = select(Jobs).where(Jobs.title == title)
        result: Jobs|None = await db.scalars(stmt).first()
        return result
    
    async def get_by_id(self, db: AsyncSession, id: int)-> Jobs|None:
            stmt = select(Jobs).where(Jobs.id == id)
            result: Jobs|None = await db.scalars(stmt).first()
            return result