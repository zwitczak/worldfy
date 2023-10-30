from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union

class AddressBase(BaseModel):
    id: Optional[int]
    country: str
    city: str
    street: str
    postal_code: str
    street_number: str
    local_number: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]

class Place(BaseModel):
    id: Optional[int]
    name: Optional[str]
    link: Optional[str]
    photo: Optional[str]
    private: bool
