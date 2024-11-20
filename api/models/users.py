from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from dependencies.database import Base


class Order(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(500), nullable=False)
    payment_method = Column(String(500), nullable=False)
