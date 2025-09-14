from pydantic import BaseModel
from datetime import datetime
from typing import List
from .product import ProductResponse

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: ProductResponse

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class CheckoutRequest(BaseModel):
    pass
