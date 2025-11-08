from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

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

    def __repr__(self):
        return f"<Promotion(id={self.id}, name={self.promotion_name}, active={self.is_active})>"
