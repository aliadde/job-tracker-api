from fastapi import FastAPI, Depends , HTTPException
from app.core.config import settings
from app.db.database import get_db

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# ============= database config  ================
from app.models.users import Users
from app.models.companies import Companies
from app.models.jobs import Jobs
# from app.models.applications import Applications
from sqlalchemy.orm import Session
from app.db.database import  engine, Base
# create all tables in the database
Base.metadata.create_all(bind=engine)

# ================================================



@app.get("/")
def root(db : Session = Depends(get_db)):
    
    return {
        "users": db.query(Users).all()
    }
