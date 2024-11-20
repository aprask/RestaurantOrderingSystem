from typing import Optional
from pydantic import BaseModel

from .restaurants import Restaurant

class CouponBase(BaseModel):
    id: int
    promo_code: str
    is_active: bool
    restaurant_id: int


class CouponCreate(CouponBase):
    pass


class CouponUpdate(BaseModel):
    id: Optional[int]
    promo_code: Optional[str]
    is_active: Optional[bool]
    restaurant_id: Optional[int]


class Coupon(CouponBase):
    id: int
    promo_code: str
    is_active: bool
    restaurant_id: Optional[Restaurant] = None


    class ConfigDict:
        from_attributes = True
