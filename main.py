from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.config import settings


async def create_tables(engine, Base):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.database import SessionLocal, engine, Base
    from app.db.seeeder import main as init_seeder

    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # seeder create jobs and statuses and positions
        await init_seeder(SessionLocal)

    yield
    
    
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ==== Routers ====
# Import the auth module AFTER creating the router
from app.api.v1 import auth , application, metadata

# Include the router from the auth module
app.include_router(auth.router, prefix='/auth',tags=["Authentication"])
app.include_router(application.router, tags=["Application"])
app.include_router(metadata.router, prefix='/metadata', tags=["Metadata"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# ==============================================