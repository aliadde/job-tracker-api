from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.applications import Applications
from app.schemas.app import CreateAppRequest, CreateAppResponse

class AppRepository:
    async def create(db: AsyncSession,data: CreateAppRequest)-> CreateAppResponse:
        new_app = Applications(**data)
        db.add(new_app)
        await db.commit()
        await db.refresh(new_app)
        return new_app
    
    async def get_company_by_name(db: AsyncSession, name: str):
        from app.models.companies import Companies
        query = select(Companies).where(Companies.name == name)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_position_by_name(db: AsyncSession, name: str):
        from app.models.positions import Positions
        
        query = select(Positions).where(Positions.name == name)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_job_by_name(db: AsyncSession, name: str):
        from app.models.jobs import Jobs
        
        query = select(Jobs).where(Jobs.name == name)
        result = await db.execute(query)
        return result.scalars().first()