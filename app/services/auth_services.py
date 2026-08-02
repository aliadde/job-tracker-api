from sqlalchemy.orm import Session
from fastapi import  status, HTTPException
from app.schemas.register import UserRegisterRequest
from app.repositories.auth import AuthRepository
from app.core.security import hash_password

# ==================================

class AuthService:

    async def register(
        self,
        db: Session,
        data: UserRegisterRequest,
        user_crud: AuthRepository 
    ):

        existing = await user_crud.get_by_email(db, data.email)

        if existing:
            # we need a ERROR handeling part for these erors
            
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

            # raise EmailAlreadyExists()

        hashed = hash_password(data.password.get_secret_value())

        user = await user_crud.create(
            db=db,
            username=data.username,
            email=data.email,
            hashed_password=hashed,
        )

        return user