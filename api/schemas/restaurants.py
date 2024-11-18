from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RestaurantBase(BaseModel):
    id: int
    restaurant_name: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    id: Optional[int]
    restaurant_name: Optional[str]


class Restaurant(RestaurantBase):
    id: int
    restaurant_name: str


    class ConfigDict:
        from_attributes = True
