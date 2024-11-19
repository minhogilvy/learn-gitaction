from pydantic import BaseModel
from typing import Dict
from pydantic import BaseModel
from typing import Optional


class WhatsAppMessage(BaseModel):
    to: str
    body: str


class InteractiveMessage(BaseModel):
    to: str
    interactive: dict


class ImageMessage(BaseModel):
    to: str
    link: str
    caption: Optional[str] = None


class VideoMessage(BaseModel):
    to: str
    link: str
    caption: Optional[str] = None


class DocumentMessage(BaseModel):
    to: str
    link: str
    filename: str
    caption: Optional[str] = None
