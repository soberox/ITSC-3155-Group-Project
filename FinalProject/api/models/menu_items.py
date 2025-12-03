from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    calories = Column(Integer)
    category = Column(String(50), nullable=False)

    # Cascade deletes from MenuItem -> Recipe at the ORM level and let DB cascade too
    recipes = relationship("Recipe", back_populates="menu_item", cascade="all, delete-orphan", passive_deletes=True)
    reviews = relationship("RatingsReviews", back_populates="menu_item")
    order_details = relationship("OrderDetail", back_populates="menu_item")
