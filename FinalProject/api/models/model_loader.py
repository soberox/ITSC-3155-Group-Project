from ..dependencies.database import Base, engine

# Import all models so they get registered with Base
from . import (
    orders,
    order_details,
    recipes,
    sandwiches,
    resources,
    customers,
    ratings_reviews,
    payment_information,
    menu_items,
    promotions
)

def index():
    # Only one call needed after all models are imported
    Base.metadata.create_all(bind=engine)
