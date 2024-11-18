from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(500))
    is_active = Column(Boolean, default=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))


