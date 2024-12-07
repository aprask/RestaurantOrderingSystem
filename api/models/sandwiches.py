from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True, server_default="null_sandwich")
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    calories = Column(Integer, nullable=False, server_default='0')
    sandwich_size = Column(String(100), nullable=False)
    is_vegetarian = Column(Boolean, nullable=False)
    is_vegan = Column(Boolean, nullable=False)
    is_gluten_free = Column(Boolean, nullable=False)
    recipes = relationship("Recipe", back_populates="sandwich", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="sandwich", cascade="all, delete-orphan")
