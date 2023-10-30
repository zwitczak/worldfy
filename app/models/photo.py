from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union

class Photo(BaseModel):
    photo_link: str
    photo_description: Optional[str]
    type: str


    class Config:
        arbitrary_types_allowed=True
        from_attributes = True
        populate_by_name = True