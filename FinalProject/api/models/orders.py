from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_number = Column(String(30), unique=True, nullable=False)
    order_status = Column(String(100), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(300))
    billing_address = Column(String(200))

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customers", back_populates="orders")

    order_details = relationship("OrderDetail", back_populates="order")
    promotions = relationship("Promotions", back_populates="order")

