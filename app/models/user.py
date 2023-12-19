from pydantic import BaseModel
from enum import Enum
from datetime import datetime, date
from typing import Optional, List, Union
from .media import Media, MediaType, MediaGet
from .localization import AddressBase
from .photo import Photo
# from .event import EventReduced


class ParticipantType(str, Enum):
    INTERESTED = 'INTERESTED'
    GOING = 'GOING'
    MAYBE = 'MAYBE'
    NOT_GOING = 'NOT_GOING'

class UserBase(BaseModel):
    id: Optional[int]
    email: Optional[str] = None
    description: Optional[str] = None
    registration_date: Optional[str] = None
    type: Optional[str] = None
    media: Optional[List[MediaGet]] = []
    photos: Optional[List[Photo]] = []

class SignUpData(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    birthday: str
    password: str
    type: str
    visible: bool


class UserCredentials(UserBase):
    nickname: Optional[str] = None
    password: str

class PrivateUser(UserBase):
    name: str
    surname: str
    nickname: str
    gender: Optional[str] = None
    birthday: Optional[date] = None
    visible: bool

class Organization(UserBase):
    name: str
    phone_number: Optional[str] = None
    organization_type: Optional[str] = None
    size: Optional[str] = None
    address: Optional[AddressBase]  = None
    
