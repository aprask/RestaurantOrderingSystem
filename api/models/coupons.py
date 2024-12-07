from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(500), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    discount = Column(DECIMAL, default=0.0)
    expir_date = Column(DateTime, default=lambda: datetime.utcnow())
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False) # Ensures cascading
    restaurant = relationship("Restaurant", back_populates="coupons")
    orders = relationship("Order", back_populates="coupons")
