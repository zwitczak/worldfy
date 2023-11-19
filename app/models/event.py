from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union
from .user import UserBase
from .photo import Photo
from .localization import AddressBase, Place
from .media import Media, MediaType, MediaGet

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
    participants_limit: Optional[str] = None
    age_limit: Optional[str]
    accepted: Optional[bool] = False
    organizers: List[UserBase]
    photos: Optional[List[Photo]]
    place: Place
    address: AddressBase
    types: List[EventType]
    media: Optional[List[Media]] = None
    

class EventGet(EventPost):
    id: int
    description: Optional[str]
    media: Optional[List[MediaGet]] = None



class EventBase(BaseModel):
    name: str
    date_start: datetime
    date_end: datetime
    is_public: bool
    description: str
    is_outdoor: bool
    
    participants_limit: Optional[str] =None
    age_limit: Optional[str] = None
    accepted: Optional[bool] = False

class EventLocalization(BaseModel):
    place: Optional[Place] = None
    address: Optional[AddressBase] = None











