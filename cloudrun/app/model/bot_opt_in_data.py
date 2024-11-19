from pydantic import BaseModel, Field
from datetime import datetime


class BotOptInData(BaseModel):
    bot_opt_in: bool = Field(alias='bot_otp_in')
    promo_opt_in: bool = Field(alias='promo_opt_in')
    privacy_agreement: bool = Field(alias='privacy_agreement')
    opt_in_date: str = Field(alias='opt_in_date')
    
    class Config:
        populate_by_name = True
