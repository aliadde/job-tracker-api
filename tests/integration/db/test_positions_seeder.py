import pytest



@pytest.mark.asyncio
async def test_prerecords_positions_created():
    import app.utils.extract_position_list as extract_position_list
    from app.models.positions import Positions
    from tests.conftest import TestSessionLocal
    from sqlalchemy import select
    from app.models.jobs import Jobs
    from tests.conftest import TestSessionLocal
    from sqlalchemy import select
    
    # ========
    # get all jobs record from database
    session = TestSessionLocal()
    stmt = select(Positions)
    result =await  session.execute(stmt)
    positions = result.scalars().all()
    await session.close()
    
    # ========
    # get all jobs names from real file list
    positions_lsit: list = extract_position_list.main()
    
    # =====
    # compare each record with real file list
    for positions1, positions2 in zip(positions, positions_lsit):
        assert positions1.position == positions2
        

