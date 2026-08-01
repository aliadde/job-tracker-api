from sqlalchemy.orm import Session
from app.models.users import Users
class AuthRepository:
    
    async def create(self, db: Session,
                    username: str, email: str, hashed_password: str):
        
        user = Users(username=username, 
                    email=email,
                    hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    async def get_by_email(self, db: Session, email: str) -> Users | None:
        return await db.query(Users).filter(Users.email == email).first()