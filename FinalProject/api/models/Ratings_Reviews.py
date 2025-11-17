from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class RatingsReviews(Base):
    __tablename__ = "RatingsReviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewText = Column(String(100), nullable=False)
    ratingScore = Column(DECIMAL(2, 1), nullable=False)

    # Foreign key to Customers table
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)

    # Relationship to Customers (one customer per review)
    customer = relationship("Customers", back_populates="reviews")
