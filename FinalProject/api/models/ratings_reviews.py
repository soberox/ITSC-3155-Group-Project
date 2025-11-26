from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class RatingsReviews(Base):
    __tablename__ = "ratings_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reviewText = Column(String(100), nullable=False)
    ratingScore = Column(DECIMAL(2, 1), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customers", back_populates="reviews")

    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    sandwich = relationship("Sandwiches", back_populates="reviews")