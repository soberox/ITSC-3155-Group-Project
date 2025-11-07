from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customers(Base):
    __tablename__ = "Customers"

    customerName = Column(String(100), nullable=False, unique=False)
    customerEmail = Column(String(100), nullable=False, unique=True)
    customerPhone = Column(String(100), nullable=False, unique=True)
    customerAddress = Column(String(100), nullable=False, unique=False)

    orders = relationship("Order", backref="customer")


