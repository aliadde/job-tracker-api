from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.register import UserRegisterRequest
from app.repositories.auth import AuthRepository
from app.core.security import hash_password

def get_auth_repository() -> AuthRepository:
    return AuthRepository()
# ==================================

class AuthService:

    async def register(
        self,
        db: Session,
        data: UserRegisterRequest,
        user_crud: AuthRepository = Depends(get_auth_repository)
    ):

        existing = await user_crud.get_by_email(db, data.email)

        if existing:
            raise Exception("This email exists")
            # raise EmailAlreadyExists()

        hashed = hash_password(data.password.get_secret_value())

        user = await user_crud.create(
            db=db,
            username=data.username,
            email=data.email,
            hashed_password=hashed,
        )

        return user