from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataConsentLog(BaseModel):
    user_id: str = Field(alias='user_id')
    action_type: str = Field(alias='action_type')
    session_id: str = Field(alias='session_id')
    timestamp: datetime = Field(alias='timestamp')
    
    class Config:
        # Allow the use of alias fields
        populate_by_name = True
