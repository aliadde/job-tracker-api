from pydantic  import BaseModel, field_validator, field_serializer
from typing import Literal
import datetime
import app.utils.extract_job_list as extract_job_list
import app.utils.extract_position_list as extract_position_list
import app.utils.extract_status_list  as extract_status_list


# =============================== Create ============================ 
class CreateAppRequest(BaseModel):
    title: str
    applied_at: datetime.datetime | None
    response_date: datetime.datetime | None
    created_at: datetime.datetime = datetime.datetime.now().isoformat()# why isoformat? becuase datetime.datetime.now() is not serializabe by python
    updated_at: datetime.datetime = datetime.datetime.now().isoformat()
    company: None | str
    status : None | str
    position: None | str
    job: None | str
    
    @field_validator('job')
    def validate_job(cls, value):
        valid_job_list = extract_job_list.main()
        if value is not None and value not in valid_job_list:
             raise ValueError(f"Job must be one of: {valid_job_list}")
        return value

    @field_validator('status')
    def validate_status(cls, value):
        valid_status_list = extract_status_list.main()
        if value is not None and value not in valid_status_list:
                raise ValueError(f"status must be one of: {valid_status_list}")
        return value


    @field_validator('position')
    def validate_position(cls, value):
        valid_position_list = extract_position_list.main()
        if value is not None and value not in valid_position_list:
                raise ValueError(f"position must be one of: {valid_position_list}")
        return value
    
    
class CreateAppResponse(BaseModel):
    id : int 
    title: str
    user_id : int | None
    applied_at: datetime.datetime | None
    response_date: datetime.datetime | None
    company_id : int | None
    position_id : int | None
    job_id : int | None
    status_id : int | None
    resume_id : int | None
    created_at : datetime.datetime
    updated_at : datetime.datetime

# =============================== Delete ============================ 
class DeleteAppRequest(BaseModel):
    id : int | None = None
    title : str | None = None
    

    
class DeleteAppResponse(BaseModel):
    id : int 
    title: str
    user_id : int | None
    applied_at: datetime.datetime | None
    response_date: datetime.datetime | None
    company_id : int | None
    position_id : int | None
    job_id : int | None
    status_id : int | None
    resume_id : int | None
    created_at : datetime.datetime
    updated_at : datetime.datetime