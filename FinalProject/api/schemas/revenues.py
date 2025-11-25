from pydantic import BaseModel

class RevenuesItem(BaseModel):
    sandwich: str
    quantity_sold: int
    revenue: float

class DailyRevenue(BaseModel):
    date: str
    total_revenue: float
