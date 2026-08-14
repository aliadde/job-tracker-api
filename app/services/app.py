import dotenv
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users
from app.models.applications import Applications
from app.models.companies import Companies
from app.models.jobs import Jobs
from app.models.positions import Positions
from app.models.statuses import Statuses
from app.repositories.app import AppRepository
from app.schemas.app import (
    CreateAppRequest,
    CreateAppResponse,
    DeleteAppResponse,
)

dotenv.load_dotenv()

class AppService: 
    async def create(
            self,
            db: AsyncSession,
            app_crud: AppRepository,
            app_data: dict,
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
            status_found: None | Statuses = await app_crud.get_status_by_name(
                db, app_data.get("status")
            )
            if status_found is not None :
                app_data["status"] = status_found.id

        # =============== position ===============
        # get position id from dtabase if exist
        if app_data.get("position") is not None:
            position_found: None | Positions = await app_crud.get_position_by_name(
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
    
    
    async def delete(
            self,
            db: AsyncSession,
            app_crud: AppRepository,
            app_data: int | str,
            user: Users
        ):
        """ 
        Delete an application.
        Proccess:
        1. if app_data is str means it is title so search for \
            title or if int means it is id so search for id of application

        2. get the application from database by id (or title)
        3. check user have access to this application or not 
        4. delete the application from database
        5. return the deleted application
        """
        # =================== 1 ===================
        found_app : Applications
        # check app data str or int
        if isinstance(app_data, int):
            found_app = await app_crud.get_app_by_id(
                db=db, 
                id=app_data
            )
        else:
            found_app = await app_crud.get_app_by_title(
                db=db, 
                title=app_data
            )
            
        # --- None found
        if found_app is None:
            raise HTTPException(status_code=404, detail="Application not found")

        # =================== 2 ===================
        if found_app.user_id != user.id:
            raise HTTPException(
                status_code=401,
                detail="You do not have access to this application"
            )
        
        
        # =================== 3 ===================
        deleted_app = await app_crud.delete_app(db=db, app=found_app)
        
        # =================== 4 ===================
        return deleted_app
    
    async def update(
            self,
            db: AsyncSession,
            app_crud: AppRepository,
            app_data: int | str,
            updated_data: dict[str, str|int|None ],
            user: Users
        ):
        """
        1. check application exist by title or id
        2. check user have access to app
        [3.] if status or job or position or company used, replace them with their id 
        4. replace fields snnt
        5. replace it in database
        """
        # ================================ 1 ================================
        if isinstance(app_data, int):
            # app_data is app id 
            found_app: Applications = await app_crud.get_app_by_id(db, app_data)
        else :
            # app_data is app title 
            found_app: Applications = await app_crud.get_app_by_title(db, app_data)
        
        
        # --- None found
        if found_app is None:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # ================================ 2 ================================
        if user.id != found_app.user_id: 
            raise HTTPException(status_code=401,detail="You do not have access to this application")

        # ================================ 3 ================================

        # =============== company ===============
        # get company full object from database with name
        if  updated_data.get("company")  and  updated_data.get("company") is not None:
            company_found: None | Companies = await app_crud.get_company_by_name(
                    db, updated_data.get("company")
                )
            if company_found is not None :
                del updated_data['company']
                updated_data["company_id"] = company_found.id

        # =============== status ===============
        # get status id from dtabase if exist
        if  updated_data.get("status")  and  updated_data.get("status") is not None:
            status_found: None | Statuses = await app_crud.get_status_by_name(
                db, updated_data.get("status")
            )
            
            if status_found is not None :
                del updated_data['status']
                updated_data["status_id"] = status_found.id

        # =============== position ===============
        # get position id from dtabase if exist
        if updated_data.get("position") and updated_data.get("position") is not None:
            position_found: None | int = await app_crud.get_position_by_name(
                db, updated_data.get("position")
            )
            if position_found is not None :
                del updated_data['position']
                updated_data["position_id"] = position_found.id

        # =============== job ===============
        # get job id from dtabase if exist
        if  updated_data.get("job") and updated_data.get("job") is not None:
            job_found: None | Jobs = await app_crud.get_job_by_name(
                db, updated_data.get("job")
            )
            
            if job_found is not None :
                del updated_data['job']
                updated_data["job_id"] = job_found.id
                
        # ================================ 4 ================================
        updated_app = await app_crud.update(db, found_app, updated_data)
        
        return updated_app