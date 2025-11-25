from datetime import date

from sqlalchemy.orm import Session


def get_total_revenues(db: Session, target_date: date):
    total_revenues = ()