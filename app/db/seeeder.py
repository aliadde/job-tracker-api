import app.utils.extract_job_list as extract_job_list


def create_jobs():
   """ 
   dump jobs to database on startup the app.
   parameters:
      job_crud: repository layer for Jobs
      
   """
   # get jobs list
   job+list = extract_job_list.main()

   # insert each job into db
   for job in job_list:
       job_crud.create(job)

