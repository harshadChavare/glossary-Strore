from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    category: str
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
