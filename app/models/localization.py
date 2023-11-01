from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union

class AddressBase(BaseModel):
    id: Optional[int] = None
    country: str
    city: str
    street: str
    postal_code: str
    street_number: str
    local_number: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Place(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    link: Optional[str] = None
    photo: Optional[str] = None
    private: bool
