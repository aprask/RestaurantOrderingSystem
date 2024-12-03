from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)

    orders = relationship("Order", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    user = relationship("User", back_populates="reviews")