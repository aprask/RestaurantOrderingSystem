from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    order_id: int
    restaurant_id: int
    user_id: int
    rating: int
    description: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    id: Optional[int]
    order_id: Optional[int]
    user_id: Optional[int]
    restaurant_id: Optional[int]
    rating: Optional[int]
    description: Optional[str]


class Review(ReviewBase):
    id: int
    

    class ConfigDict:
        from_attributes = True
