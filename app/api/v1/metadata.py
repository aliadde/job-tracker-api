from fastapi import APIRouter, status, Depends
from app.services.metadata import MetadataService
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.positions import PositionRepository
from app.repositories.status import StatusRepository
from app.repositories.jobs import JobRepository
from app.repositories.company import CompanyRepository

from app.schemas.company import CreateCompanyRequest,CreateCompanyResponse

from app.db.database import get_db
# ========================== Router ==================================
router = APIRouter()
# ======================== Dependency injection ===========================
def position_crud():
    return PositionRepository()

def status_crud():
    return StatusRepository()

def job_crud():
    return JobRepository()

def company_crud():
    return CompanyRepository()

def metadata_service():
    return MetadataService()

# ============================= Endpoints ===============================

@router.get("/status", status_code=status.HTTP_200_OK)
async def get_all_statuses(
    db: AsyncSession = Depends(get_db),
    status_crud: StatusRepository =Depends(status_crud),
    metadata_service: MetadataService = Depends(metadata_service),
):
    return await metadata_service.get_all_status(
        db=db,
        status_crud=status_crud,
    )
    

@router.get("/job", status_code=status.HTTP_200_OK)
async def get_all_jobs(
    db: AsyncSession = Depends(get_db),
    job_crud: JobRepository = Depends(job_crud),
    metadata_service: MetadataService = Depends(metadata_service),
):
    return await metadata_service.get_all_job(
        db=db,
        job_crud=job_crud,
    )


@router.get("/position", status_code=status.HTTP_200_OK)
async def get_all_positions(
    db: AsyncSession = Depends(get_db),
    position_crud: PositionRepository = Depends(position_crud),
    metadata_service: MetadataService = Depends(metadata_service),
):
    return await metadata_service.get_all_position(
        db=db,
        position_crud=position_crud,
    )

@router.post("/company", status_code=status.HTTP_201_CREATED, response_model=CreateCompanyResponse)
async def add_company(
    company: CreateCompanyRequest,
    db: AsyncSession = Depends(get_db),
    company_crud: CompanyRepository = Depends(company_crud),
    metadata_service: MetadataService = Depends(metadata_service),
):
    return await metadata_service.create_company(
        db=db,
        company_crud=company_crud,
        company=company
    )
