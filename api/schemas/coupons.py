from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .restaurants import Restaurant

class CouponBase(BaseModel):
    id: int
    promo_code: str
    is_active: bool
    restaurant_id: int
    discount: float
    expir_date: datetime


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    id: Optional[int]
    promo_code: Optional[str]
    is_active: Optional[bool]
    restaurant_id: Optional[int]
    discount: Optional[float]
    expir_date: Optional[datetime]


class Coupon(CouponBase):
    id: int
    promo_code: str
    is_active: bool
    restaurant_id: Optional[int] = None
    discount: Optional[float] = None
    expir_date: Optional[datetime] = None


    class ConfigDict:
        from_attributes = True
