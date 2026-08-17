from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.positions import PositionRepository
from app.repositories.status import StatusRepository
from app.repositories.jobs import JobRepository


class MetadataService:
    
    async def get_all_status(
        self,
        db: AsyncSession,
        status_crud: StatusRepository,
    ):
        return await status_crud.get_all(db=db)

    
    async def get_all_job(
        self,
        db: AsyncSession,
        job_crud: JobRepository,
    ):
        return await job_crud.get_all(db=db)



    async def get_all_position(
        self,
        db: AsyncSession,
        position_crud: PositionRepository,
    ):
        return await position_crud.get_all(db=db)