from pydantic import BaseModel
from typing import Optional, Dict, Any


class APIResponse():
    def __init__(
        self,
        api_version="v1",
        status_code=200,
        message="Success",
        data=None
    ):
        """
        Initialize the APIResponse with default parameters.

        Args:
            api_version (str): The version of the API. Default is "v1".
            status_code (int): The HTTP status code. Default is 200.
            message (str): The message describing the response. Default is "Success".
            data (any): The data to be included in the response. Default is None.
        """
        self.api_version = api_version
        self.status_code = status_code
        self.message = message
        self.data = data
    
    def generate_response(
        self,
        api_version=None,
        status_code=None,
        message=None,
        data=None
    ):
        if api_version == None:
            api_version = self.api_version
        if status_code == None:
            status_code = self.status_code
        if message == None:
            message = self.message
        if data == None:
            data = self.data
        
        response = {
            "api_version": api_version,
            "status_code": status_code,
            "message": message,
            "data": data
        }
        
        return response


class APIResponse(BaseModel):
    code: int
    message: str
    data: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "OK",
                "data": {},
            }
        }

class TaskStatus:
    PENDING: str = 'PENDING'
    QUEUED: str = 'QUEUED'
    SUCCESS: str = 'SUCCESS'
    ERROR: str = 'ERROR'

    def is_done(self) -> bool:
        return self in (self.SUCCESS, self.ERROR)
