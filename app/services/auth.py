import dotenv, os
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException
import app.schemas.register as schema_register
import app.schemas.login as schema_login
from app.repositories.auth import AuthRepository
from app.core.security import (hash_password,
                               verify_password,
                               create_jwt_token)
from app.models.users import Users

dotenv.load_dotenv()
# ==================================

class AuthService:

    async def register(
        self,
        db: Session,
        data: schema_register.UserRegisterRequest,
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
    
    async def login(
        self,
        db: Session,
        data: schema_login.UserLoginRequest,
        user_crud: AuthRepository 
    ):

        # is user valid user?
        # username check
        user: Users | None = await user_crud.get_by_username(
            db=db, username=data.username
        )
        if user : 
            # password check
            password_check:bool = verify_password(
                data.passowrd,
                user.hashed_password
            )

            if password_check:
        
                # create jwt token for user, return jwt token to user  
                payload: schema_login.JWTPayload={
                    "id": user.id,
                    "username": user.username
                }
                
                jwt_token = create_jwt_token(
                        payload=payload,
                        public_key=os.getenv("SECRET_KEY")
                    )
                
                return {"access_token":jwt_token,"token_type": "bearer"}
            
            
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail="invalid username or password")
