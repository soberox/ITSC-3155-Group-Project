from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    customer_name: str
    item_name: str
    order_status: str
    order_type: str
    tracking_number: str
    billing_address: str
    # DB uses DECIMAL(10,2) for amount — accept float in the schema
    amount: float


class OrderDetailCreate(BaseModel):
    order_id: int
    menu_item_id: int

class OrderDetailUpdate(BaseModel):
    customer_name: Optional[str] = None
    item_name: Optional[str] = None
    order_status: Optional[str] = None
    order_type: Optional[str] = None
    billing_address: Optional[str] = None
    amount: Optional[float] = None

class StatusUpdate(BaseModel):
    id: int
    order_status: str

class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_items: MenuItem = Optional[MenuItem]

    class ConfigDict:
        from_attributes = True