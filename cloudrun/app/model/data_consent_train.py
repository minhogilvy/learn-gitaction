from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DataConsentTrain(BaseModel):
    user_id: Optional[str] = Field(default=None, alias='userId')
    calculus_grade: Optional[int] = Field(default=None, alias='calculusGrade')
    caries_grade: Optional[int] = Field(default=None, alias='cariesGrade')
    consent: Optional[bool] = Field(default=None, alias='consent')
    created_at: Optional[datetime] = Field(default=None, alias='createdAt')
    discoloration_grade: Optional[int] = Field(default=None, alias='discolorationGrade')
    gingivitis_grade: Optional[int] = Field(default=None, alias='gingivitisGrade')
    image_path: Optional[str] = Field(default=None, alias='imagePath')
    mouth_ulcer_grade: Optional[int] = Field(default=None, alias='mouthUlcerGrade')
    pov: Optional[str] = Field(default=None, alias='pov')
    status: Optional[str] = Field(default="waiting", alias='status')
    
    
    class Config:
        populate_by_name = True
