from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..dependencies.database import Base

class Promotions(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    promotion_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    generate_date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    order = relationship("Order", back_populates="promotions")
