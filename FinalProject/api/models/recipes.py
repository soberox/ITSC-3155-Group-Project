from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="CASCADE", onupdate="CASCADE"))
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="CASCADE", onupdate="CASCADE"))
    amount = Column(Integer, index=True, nullable=False, server_default='0')

    # Let the DB handle deletes/updates; enable passive_deletes so ORM doesn't try to nullify
    menu_item = relationship("MenuItem", back_populates="recipes", passive_deletes=True)
    resource = relationship("Resource", back_populates="recipes", passive_deletes=True)
