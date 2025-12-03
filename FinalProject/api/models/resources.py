from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0')
    unit = Column(String(20), nullable=False, default='unit')

    # Cascade deletes from Resource -> Recipe at ORM level and let DB cascade too
    recipes = relationship("Recipe", back_populates="resource", cascade="all, delete-orphan", passive_deletes=True)
