from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataAuditTrailLog(BaseModel):
    user_id: Optional[str] = Field(default=None, alias='user_id')
    user_request_delete: Optional[datetime] = Field(default=None, alias='user_request_delete')
    system_delete: Optional[datetime] = Field(default=None, alias='system_delete')
    timestamp: Optional[datetime] = Field(default=None, alias='timestamp')
    
    class Config:
        populate_by_name = True