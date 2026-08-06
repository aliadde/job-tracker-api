from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import Users
class AuthRepository:
    
    async def create(self, db: AsyncSession,
                    username: str, email: str, hashed_password: str):
        
        user = Users(
            username=username, 
            email=email,
            hashed_password=hashed_password
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def get_by_email(self, db: AsyncSession, email: str
                    ) -> Users | None:
        
        stmt = select(Users).where(Users.email == email)
        results = await db.execute(stmt)
        user = results.scalar_one_or_none()
        return user

    async def get_by_username(self, db: AsyncSession, username: str)-> Users|None:
        stmt = select(Users).where(Users.username == username)
        result: Users|None = await db.scalars(stmt).first()
        return result
        