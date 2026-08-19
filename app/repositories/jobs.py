from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Jobs

class JobRepository:
    
    async def create(self, db: AsyncSession, title: str):
        from app.models.jobs import Jobs

        job = Jobs(title=title)

        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job


    async def get_all(self, db: AsyncSession):
        from app.models.jobs import Jobs
        stmt = select(Jobs)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    
    async def get_by_job_title(self, db: AsyncSession, title: str)-> Jobs|None:
        from app.models.jobs import Jobs
        stmt = select(Jobs).options(selectinload(Jobs.applications)).where(Jobs.title == title)
        result = await db.execute(stmt)
        return result.scalars().first()
    
    async def get_by_id(self, db: AsyncSession, id: int)-> Jobs|None:
            from app.models.jobs import Jobs
            stmt = select(Jobs).options(selectinload(Jobs.applications)).where(Jobs.id == id)
            result = await db.execute(stmt)
            return result.scalars().first()