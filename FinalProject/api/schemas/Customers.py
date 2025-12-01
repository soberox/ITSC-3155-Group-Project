from typing import Optional, List
from pydantic import BaseModel

# Base schema shared between Create and Read
class CustomerBase(BaseModel):
    id: int
    customerName: str
    customerEmail: str
    customerPhone: str
    customerAddress: str


# Schema used when creating a customer (request body)
class CustomerCreate(CustomerBase):
    pass

# Schema used when updating a customer (request body)
class CustomerUpdate(CustomerBase):
    id: Optional[int] = None
    customerName: Optional[str] = None
    customerEmail: Optional[str] = None
    customerPhone: Optional[str] = None
    customerAddress: Optional[str] = None

# Schema used when returning a customer from the API
class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True  # Enables SQLAlchemy model -> Pydantic conversion