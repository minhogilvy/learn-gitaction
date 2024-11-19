from pydantic import BaseModel, Field
from typing import Optional


class DataFlowExtend(BaseModel):
    flow_extend: bool = Field(alias='flow_extend')
    name_flow_extend: str = Field(alias='name_flow_extend')

    class Config:
        # Allow the use of alias fields
        populate_by_name = True
