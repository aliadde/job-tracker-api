from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.app import AppRepository
from app.schemas.app import CreateAppRequest, CreateAppResponse
from fastapi import HTTPException, status
from app.models.companies import Companies
import dotenv
from app.models import Users
dotenv.load_dotenv()

class AppService: 
    async def create(
            self,
            db: AsyncSession,
            app_crud: AppRepository,
            app_data: CreateAppRequest,
            user: Users
        ):
        """ 
        first we check user inputs. 
        compony, status, position and job must be id not name in databse. 
        so first of all we have to change these value to id given from database.
        then we can dump new app to database.
        """
        
        # =============== company  ===============
        # if company have been set 
        if app_data.get("company") is not None:
            
            # get compay fro dtabase (repository)
            company_found: None | Companies  = await app_crud.get_company_by_name(
                db, app_data.get("company")
            )
            if company_found is None :
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail=f"Company with name {app_data.get("company")} not found"
                )
            
            # update the user data with the company id from the database
            app_data["company"] = company_found.id
            
        
        # =============== status ===============
        # get status id from dtabase if exist
        if app_data.get("status") is not None:
            status_found: None | int = await app_crud.get_status_by_name(
                db, app_data.get("status")
            )
            if status_found is not None :
                app_data["status"] = status_found.id

        # =============== position ===============
        # get position id from dtabase if exist
        if app_data.get("position") is not None:
            position_found: None | int = await app_crud.get_position_by_name(
                db, app_data.get("position")
            )
            if position_found is not None :
                app_data["position"] = position_found.id

        # =============== job ===============
        # get job id from dtabase if exist
        if app_data.get("job") is not None:
            from app.models import Jobs
            job_found: None | Jobs = await app_crud.get_job_by_name(
                db, app_data.get("job")
            )
            
            if job_found is not None :
                app_data["job"] = job_found.id

        # ===================== add user id data ======================
        app_data["user_id"] = user.id
        
        # ==================== App creation ====================
        # Create a new application record in the database
        new_app: CreateAppResponse = await app_crud.create(db, app_data)
        
        return new_app
        
