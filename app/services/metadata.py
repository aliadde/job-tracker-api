from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.positions import PositionRepository
from app.repositories.status import StatusRepository
from app.repositories.jobs import JobRepository
from app.repositories.company import CompanyRepository
from app.models.companies import Companies
from app.schemas.company import CreateCompanyRequest, CreateCompanyResponse
from fastapi import HTTPException, status

class MetadataService:
    
    async def create_company(
        self,
        db: AsyncSession,
        company_crud: CompanyRepository ,
        company: CreateCompanyRequest,
    ):
        """
        Create new company.

        Args:
            company: new company data.

        Returns:
            New company created object.

        Raises:
            HTTPException: status code 409 if the a company with same name exist in database.

        """
        # get by name if exist raise eerror
        found_company: Companies | None = await company_crud.get_by_name(
            db=db,name=company.name
        )
        if not found_company:
            HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This company already exist."
            )

        # creae object
        company: Companies = Companies(
            name=company.name,
            location=company.location,
        )

        created_company= await company_crud.create(
            db=db, company=company
        )

        return CreateCompanyResponse(
            id=created_company.id,
            name=created_company.name,
            location=created_company.location,
        )

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