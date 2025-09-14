# schemas.py

from pydantic import BaseModel
from typing import Optional


# Glossary schemas (unchanged)
class GlossaryBase(BaseModel):
    term: str
    definition: str
    example: Optional[str] = None

class GlossaryCreate(GlossaryBase):
    pass

class GlossaryOut(GlossaryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Product schemas
class ProductBase(BaseModel):
    category: str
    name: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductOut(BaseModel):
    id: int
    category: str
    name: str
    price: float
    stock: int

    class Config:
        orm_mode = True


# Cart item for products
class ProductCartItemOut(BaseModel):
    id: int
    product: ProductOut

    class Config:
        from_attributes = True
