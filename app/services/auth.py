import dotenv, os
from sqlalchemy.orm import Session
from fastapi import  status, HTTPException
import app.schemas.register as schema_register
import app.schemas.login as schema_login
from app.repositories.auth import AuthRepository
from app.core.security import (
    hash_password, verify_password, create_jwt_token, decode_jwt_token
)

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
    )-> schema_register.UserRegisterResponse:
        """ 
            This function will register a new user in the database.
            at frist check user exist with same email. if anyone exist an execption raise.
            then hash the user password. finally dump user to databse and return same user object from database.

            :param db: AsyncSession - The database session to use for the operation.
            :param data: schema_register.UserRegisterRequest - The user registration data.
            :user_crud: AuthRepository - The repository to interact with the users table.
            :return: schema_register.UserRegisterResponse - The registered user information.
        """
        existing = await user_crud.get_by_email(db, data.email)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

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
    )-> schema_login.UserLoginResponse:
        """ 
           this function will login the user and generate a JWT token for them. 
            it will check if the user exists in the database or not.
            if the user exists then it will check if the password is correct or not.
            if the password is correct then it will create a JWT token for the user and return it to the user. 
        """
        # is user valid user?
        # username check
        user: Users | None = await user_crud.get_by_username(
            db=db, username=data.username
        )
        if user : 
            # is user active or not
            if user.is_active :
                
                # password check
                password_check:bool = verify_password(
                    data.password,
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
            
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is inactive",
                )
                
            
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail="invalid username or password")

    async def get_current_user(
        self,
        user: Users,
        db: AsyncSession,
        user_crud:  AuthRepository
    ) -> Users:

        # return some data from user
        ready_user = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "update_at": user.update_at,
            "applications": [application.title for application in user.applications]
        }
        return ready_user

    async def delete(
        self,
        user: Users,
        db: Session,
        user_crud: AuthRepository,
    )-> Users:
        """
        Delete user.
        User can delete itself account.

        Args:
            user: current user logged in object ``app.models.users class Users``.

        Returns:
            Return the deleted user.

        Raises:

        """
        deleted_user: Users =  await user_crud.delete(
            db=db,
            user=user,
        )
        # convert Users class object to dictionary
        deleted_user = deleted_user.__dict__
        del deleted_user['hashed_password']
        del deleted_user['_sa_instance_state']
        return deleted_user

    async def validate_token(
        self,
        token: str ,
        db: AsyncSession,
        user_crud:  AuthRepository
    )-> Users:
        """
            This method validate the token sent from user.
            It will check the token is valid or not and also it will extract the payload from token. 
            If the token is invalid then it will raise an exception with status code 401 Unauthorized.
            If the token is valid then it will return the user object from database completly.
        """
        # user payload extract
        current_user = decode_jwt_token(token,public_key=os.getenv("SECRET_KEY"))
        # result: `payload stored in jwt token` Exception raise: InvalidToken, ExpiredToken
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # query database and return user object completly
        found_user = await user_crud.get_by_username(
            db=db,
            username=current_user.get("username")
        )
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # return complete user object
        return found_user
