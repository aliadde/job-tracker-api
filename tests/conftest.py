import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.db.database import get_db
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield TestSessionLocal()
    Base.metadata.drop_all(bind=engine) 
    
@pytest.fixture(scope="function", autouse=True)
def db_session(setup_db):
    db = setup_db
    try:
        yield db
    finally:
        db.close()
        

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    
    from main import app
    app.dependency_overrides[get_db] = override_get_db
    
    # ==== This is one way :
    # return app.test_client() 
    
    # ====== another way
    with TestClient(app) as client:
        yield client
    # app.dependency_overrides.clear()