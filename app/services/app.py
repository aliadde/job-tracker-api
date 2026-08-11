from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.app import AppRepository

import dotenv
dotenv.load_dotenv()

class AppService: 
    async def create(
            self,
            db: AsyncSession,
            app_crud: AppRepository
        ):
        # Create a new application record in the database
        # app_crud.create(db, )
        pass