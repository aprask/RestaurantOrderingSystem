from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_name = Column(String(500), nullable=False)
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="restaurant", cascade="all, delete-orphan")

