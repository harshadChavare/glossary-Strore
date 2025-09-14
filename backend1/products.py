# routers/products.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Product, ProductCartItem
from schemas import ProductCreate, ProductOut, ProductCartItemOut
from auth import get_current_user
from database import get_db

router = APIRouter()


@router.get("/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/products", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.post("/products/cart/add/{product_id}")
def add_product_to_cart(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(ProductCartItem).filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Product already in cart")

    cart_item = ProductCartItem(user_id=user.id, product_id=product_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": f"Added '{product.name}' to cart."}


@router.get("/products/cart", response_model=List[ProductCartItemOut])
def get_product_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(ProductCartItem).filter(ProductCartItem.user_id == user.id).all()


@router.delete("/products/cart/remove/{item_id}")
def remove_product_from_cart(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(ProductCartItem).filter(ProductCartItem.id == item_id, ProductCartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"message": "Removed from cart"}


@router.post("/products/cart/purchase")
def purchase_products(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(ProductCartItem).filter(ProductCartItem.user_id == user.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Simulate purchase by deleting cart items
    for item in items:
        db.delete(item)
    db.commit()
    return {"message": "Purchase successful!"}
