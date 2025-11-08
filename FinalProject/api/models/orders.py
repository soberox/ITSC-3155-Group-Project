from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    traking_number = Column(String(30), unique=True, nullable=False)
    customer_name = Column(String(100))
    order_status = Column(String(100), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    customer_name = Column(String(100), ForeignKey("customer.customer_name"))
    billing_address = Column(String(200), ForeignKey("customer.address"))   