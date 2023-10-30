from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List, Union

class UserBase(BaseModel):
    id: Optional[int]
    name: Optional[str]