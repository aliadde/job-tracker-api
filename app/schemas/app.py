from pydantic  import BaseModel
import datetime

class CreateAppRequest(BaseModel):
    title: str
    applied_at: datetime.datetime | None
    response_date: datetime.datetime | None
    created_at: datetime.datetime = datetime.datetime.now()
    update_at: datetime.datetime = datetime.datetime.now()
    