import dotenv, os
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException
import app.schemas.register as schema_register
import app.schemas.login as schema_login
from app.repositories.auth import AuthRepository
from app.core.security import (hash_password,
                               verify_password,
                               create_jwt_token,
                               decode_jwt_token)
from app.models.users import Users
from sqlalchemy.ext.asyncio import AsyncSession
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
                    "username": user.username,
                    "active": user.is_active
                }
                
                jwt_token = create_jwt_token(
                        payload=payload,
                        public_key=os.getenv("SECRET_KEY")
                    )
                
                return {"access_token":jwt_token,"token_type": "bearer"}
            
            
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail="invalid username or password")


    async def get_current_user(
            self,
            token: str ,
            db: AsyncSession,
            user_crud:  AuthRepository
        ) -> Users:
        
        # user payload extract
        current_user = decode_jwt_token(token)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # check active or not
        if current_user.get("active") == False:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        # query database and return user object completly
        found_user = await user_crud.get_by_username(db=db, username=current_user.get("username"))
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # return some data from user
        ready_user = {
            "id": found_user.id,
            "username": found_user.username,
            "email": found_user.email,
            "active": found_user.active,
            "created_at": found_user.created_at,
            "update_at": found_user.update_at,
            "companies": [company.name for company in found_user.companies],
            "applications": [application.title for application in found_user.applications]
        }
        return ready_user