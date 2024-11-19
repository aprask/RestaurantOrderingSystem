from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    customer_name: str
    payment_method: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    id: Optional[int]
    customer_name: Optional[str] = None
    payment_method: Optional[str] = None
    


class User(UserBase):
    id: int
    customer_name: str
    payment_method: str


    class ConfigDict:
        from_attributes = True
