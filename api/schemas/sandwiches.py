from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class SandwichBase(BaseModel):
    id: int
    sandwich_name: str
    price: float
    calories: int
    sandwich_size: str
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool

class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    id: Optional[int]
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[float] = None
    sandwich_size: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None


class Sandwich(SandwichBase):
    id: int
    sandwich_name: str
    price: float
    calories: float
    sandwich_size: str
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool

    class ConfigDict:
        from_attributes = True