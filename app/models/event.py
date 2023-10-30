from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union
from .user import UserBase
from .photo import Photo
from .localization import AddressBase, Place

class EventType(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]

class EventPost(BaseModel):
    name: str
    date_start: datetime
    date_end: datetime
    is_public: bool
    description: str
    is_outdoor: Optional[bool]
    participants_limit: Optional[str]
    age_limit: Optional[str]
    organizers: List[UserBase]
    photos: Optional[List[Photo]]
    place: Place
    address: AddressBase
    types: List[EventType]

    
class EventGet(EventPost):
    id: int











