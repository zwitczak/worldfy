from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union

class Photo(BaseModel):
    id: Optional[int] = None
    photo_link: Optional[str] =None
    photo_description: Optional[str]
    type: Optional[str] = None
    datetime_posted: Optional[datetime] = None


    class Config:
        arbitrary_types_allowed=True
        from_attributes = True
        populate_by_name = True