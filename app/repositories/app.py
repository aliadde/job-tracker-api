from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.applications import Applications
from app.schemas.app import CreateAppRequest, CreateAppResponse

class AppRepository:
    async def create(self, db: AsyncSession,data: CreateAppRequest)-> CreateAppResponse:
        new_app = Applications(
            title=data.get("title"),
            applied_at=data.get("applied_at"),
            response_date=data.get("response_date"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            company_id=data.get("company"),
            user_id=data.get("user_id"),
            status_id=data.get("status"),
            position_id=data.get("position"),
            job_id=data.get("job"),
        )
        db.add(new_app)
        await db.commit()
        await db.refresh(new_app)
        return new_app
    
    async def get_company_by_name(self, db: AsyncSession, name: str):
        from app.models.companies import Companies
        query = select(Companies).where(Companies.name == name)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_position_by_name(self, db: AsyncSession, position: str):
        from app.models.positions import Positions
        
        query = select(Positions).where(Positions.position == position)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_job_by_name(slef, db: AsyncSession, title: str):
        from app.models.jobs import Jobs
        
        query = select(Jobs).where(Jobs.title == title)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_status_by_name(slef, db: AsyncSession, status: str):
        from app.models import Statuses
        
        query = select(Statuses).where(Statuses.status == status)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_app_by_id(self, db: AsyncSession, id: int):
        from app.models import Applications
        query = select(Applications).where(Applications.id == id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_app_by_title(self, db: AsyncSession, title: str):
        from app.models import Applications
        query = select(Applications).where(Applications.title == title)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def delete_app(self, db: AsyncSession, app: Applications):
        # now deleting the app
        await db.delete(app)
        await db.commit()
        # return deleted app to user
        return app
    
    async def update(self, db: AsyncSession, app: Applications, updated_data: dict[str, any]):
        # change fields and value of them
        for key, value in updated_data.items():
            setattr(app, key, value)
        
        db.commit()
        db.refresh(app)
        return app