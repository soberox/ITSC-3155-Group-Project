from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    tracking_number: str
    customer_name: str
    item_name: str
    order_status: str
    order_type: str
    amount: float
    billing_address: Optional[str] = None

class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None
    order_status: Optional[str] = None

class StatusUpdate(BaseModel):
    id: int
    order_status: str

class OrderDetail(OrderDetailBase):
    id: int
    menu_item: Optional[MenuItem] = None  # FIX name to match model

    class ConfigDict:
        from_attributes = True