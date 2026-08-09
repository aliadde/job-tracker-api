import pytest



@pytest.mark.asyncio
async def test_prerecords_jobs_created():
    import app.utils.extract_status_list as extract_status_list
    from app.models.statuses import Statuses
    from tests.conftest import TestSessionLocal
    from sqlalchemy import select
    
    # ========
    # get all jobs record from database
    session = TestSessionLocal()
    stmt = select(Statuses)
    result =await  session.execute(stmt)
    statuses = result.scalars().all()
    await session.close()
    
    # ========
    # get all jobs names from real file list
    status_list: list = extract_status_list.main()
    
    # =====
    # compare each record with real file list
    for status1, status2 in zip(statuses , status_list):
        assert status1.status == status2
        

