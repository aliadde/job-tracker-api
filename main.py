from fastapi import FastAPI, Depends , APIRouter
from app.core.config import settings
from app.db.database import get_db

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)
router = APIRouter()

# Import the auth module AFTER creating the router
from app.api.v1 import auth  # Import the module, not the router

# Include the router from the auth module
app.include_router(auth.router)  # Include the router with prefix


if __name__ == "__main__":
    import uvicorn
    # ============= database config  ================
    from app.db.database import  engine, Base
    # create all tables in the database
    Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=8000) 
# ==============================================