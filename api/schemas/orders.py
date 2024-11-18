from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .sandwiches import Sandwich
from .restaurants import Restaurant


class OrderBase(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    description: Optional[str] = None
    sandwich_id: int
    amount: float
    restaurant_id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    order_date: Optional[datetime]
    description: Optional[str]
    sandwich_id: Optional[int]
    amount: Optional[float]
    restaurant_id: Optional[int]


class Order(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    description: Optional[str] = None
    sandwich_id: Sandwich = None
    order_date: Optional[datetime] = None
    amount: float
    restaurant_id: Restaurant = None


    class ConfigDict:
        from_attributes = True
