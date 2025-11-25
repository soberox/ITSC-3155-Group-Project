from datetime import date

from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session

from ..models.order_details import OrderDetail
from ..models.orders import Order
from ..models.sandwiches import Sandwich


def get_total_revenues(db: Session, target_date: date):
    total_revenues = (db.query(func.sum(OrderDetail.amount * Sandwich.price))
                      .join(Order, Order.id == OrderDetail.order_id)
                      .join(Sandwich, Sandwich.id == OrderDetail.sandwich_id)
                      .filter(cast(Order.order_date, Date) == target_date))
    total_amount = total_revenues.scalar()

    if total_amount is None:
        return 0.0

    return float(total_amount)
