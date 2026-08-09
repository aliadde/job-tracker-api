import pytest



@pytest.mark.asyncio
async def test_prerecords_jobs_created():
    import app.utils.extract_job_list as extract_job_list
    from app.models.jobs import Jobs
    from tests.conftest import TestSessionLocal
    from sqlalchemy import select
    
    # ========
    # get all jobs record from database
    session = TestSessionLocal()
    stmt = select(Jobs)
    result =await  session.execute(stmt)
    jobs = result.scalars().all()
    await session.close()
    
    # ========
    # get all jobs names from real file list
    job_lsit: list = extract_job_list.main()
    
    # =====
    # compare each record with real file list
    for job1, job2 in zip(jobs , job_lsit):
        assert job1.title == job2
        

