import app.utils.extract_job_list as extract_job_list
from app.repositories.jobs import JobRepository
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

class Seeder:
   def __init__(self, db: AsyncSession, job_crud: JobRepository):
      self.db = db
      self.job_crud = job_crud


   async def create_jobs(self, extract_job_list:function):
      """ 
      dump jobs to database on startup the app.
      parameters:
         job_crud: repository layer for Jobs
         
      """
      #  =================================
      # Jobs 
      #  =================================
      # get jobs list
      job_list = extract_job_list.main()

      # insert each job into db
      for job in job_list:
         await self.job_crud.create(title=job , db=self.db)

   # async def create_statuses(self, extract_statuses_list: function):
   #    #  =================================
   #    # statuses 
   #    #  =================================
   #    statuses_list = extract_statuses_list.main()
   #    for status in statuses_list:
   #       await self.status_crud.create(status=status , db=self.db)
   
   # async async def create_statuses(self, extract_positions_list: function):
   #    #  =================================
   #    # Positions
   #    #  =================================
   #    positions_list = extract_positions_list.main()
   #    for position in positions_list:
   #       await self.position_crud.create(position=position , db=self.db)

async def main():
   from app.db.database  import SessionLocal
   # create seession
   with SessionLocal() as session:
      # create instanse from seeder
      seeder = Seeder(
         db=session,
         job_crud=JobRepository()
      )
      # dump jobs to database
      await seeder.create_jobs(extract_job_list=extract_job_list)
      """       
      # dump statuses to database
      await seeder.create_statuses(extract_positions_list=extract_positions_list)

      # dump positions to database
      await seeder.create_positions(extract_positions_list=extract_positions_list)
      """

if __name__ == "__main__":
   asyncio.run(main())