from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
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