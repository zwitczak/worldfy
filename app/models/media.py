from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union


class MediaType(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None

class Media(BaseModel):
    id: Optional[int] = None
    link: str
    type_id: int

    class Config:
        arbitrary_types_allowed=True
        from_attributes = True
        populate_by_name = True

class MediaGet(BaseModel):
    id: Optional[int] = None
    link: str
    type_name: str
    media_icon: Optional[str] = None

    class Config:
        arbitrary_types_allowed=True
        from_attributes = True
        populate_by_name = True

