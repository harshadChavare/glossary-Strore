from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.user import User
from ...models.product import Product
from ...models.order import Order
from ...schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ...schemas.order import OrderResponse
from ...dependencies import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/products", response_model=List[ProductResponse])
def get_all_products_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    return products

@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    return orders

@router.get("/users")
def get_all_users_admin(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
