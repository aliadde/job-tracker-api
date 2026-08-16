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
        token: str ,
        db: AsyncSession,
        user_crud:  AuthRepository
    ) -> Users:
        """ 
            This method will be used to get the current logged in user from token.
            It will decode the token and check if it is valid or not. If it is valid then it will return the user object from database.
            If it is not valid then it will raise an exception.
        """
        # user payload extract
        current_user = decode_jwt_token(token,public_key=os.getenv("SECRET_KEY"))
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
            "is_active": found_user.is_active,
            "created_at": found_user.created_at,
            "update_at": found_user.update_at,
            "applications": [application.title for application in found_user.applications]
        }
        return ready_user
    
    async def delete(
        self,
        user_id: int,
        db: Session,
        user_crud: AuthRepository,
    )-> Users:
        """
        Delete user.
        This service get user from database by id, then will delete the user.

        Args:
            user_id: id of the user.

        Returns:
            Return the deleted user.

        Raises:
            HTTPException: status code 404 if user not found by that id.

        """
        user = await user_crud.get_by_id(db=db, id=user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return await user_crud.delete(
            db=db,
            user=user,
        )

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