from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.users import Users
class AuthRepository:

    async def create(
        self,
        db: AsyncSession,
        username: str,
        email: str,
        hashed_password: str
    ):

        user = Users(
            username=username, 
            email=email,
            hashed_password=hashed_password
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete(self,db:AsyncSession, user: Users):
        await db.delete(user)
        await db.commit()
        return user

    async def get_by_email(self, db: AsyncSession, email: str
                    ) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        results = await db.execute(stmt)
        user = results.scalar_one_or_none()
        return user

    async def get_by_username(self, db: AsyncSession, username: str)-> Users|None:
        stmt = select(Users).options(selectinload(Users.applications)).where(Users.username == username)
        result: Users|None = await db.scalars(stmt)
        return result.first()
    
    async def get_by_id(self, db: AsyncSession, id: int)-> Users|None:
            stmt = select(Users).options(selectinload(Users.applications)).where(Users.username == id)
            result: Users|None = await db.scalars(stmt)
            return result.first()