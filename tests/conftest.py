import  os, pytest_asyncio, pytest
from app.db.database import get_db, Base
from fastapi.testclient import TestClient
import main
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.seeeder import main as init_seeder


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await init_seeder(TestSessionLocal)


@pytest.fixture(scope="session", autouse=True)
def tear_down():
    """ end of the tests.
    It will remove the test.db file after the tests are done.
    """
    yield
    os.remove("test.db")

@pytest.fixture()
def client():
    return TestClient(main.app)

async def override_get_db():
    session = TestSessionLocal()
    try:
        yield session 
    finally:
        await session.close()

main.app.dependency_overrides[get_db] = override_get_db