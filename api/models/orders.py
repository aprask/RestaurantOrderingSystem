from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Ensure CASCADE here
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300), nullable=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL, index=True, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    delivery_method = Column(String(300), nullable=False)
    status_of_order = Column(String(300), nullable=False, server_default="pending")
    promo_code = Column(String(300), ForeignKey("coupons.promo_code", ondelete="SET NULL"), nullable=True)
    sandwich = relationship("Sandwich", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    user = relationship("User", back_populates="orders")
    reviews = relationship("Review", back_populates="orders", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="orders")
