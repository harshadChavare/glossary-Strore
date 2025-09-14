from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import CartItem, Purchase, Glossary
from schemas import CartItemCreate, CartItemOut, PurchaseCreate, PurchaseOut
from auth import get_current_user
from database import get_db

router = APIRouter()

@router.get("/cart", response_model=List[CartItemOut])
def get_cart_items(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(CartItem).filter(CartItem.user_id == user.id).all()

@router.post("/cart", response_model=CartItemOut)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_item = CartItem(**item.dict(), user_id=user.id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/cart/{item_id}")
def delete_cart_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.post("/purchase", response_model=PurchaseOut)
def make_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    purchase_record = Purchase(user_id=user.id, details=purchase.details)
    db.add(purchase_record)
    db.commit()
    db.refresh(purchase_record)
    return purchase_record

@router.post("/cart/add/{glossary_id}")
def add_to_cart_by_glossary(glossary_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    glossary_term = db.query(Glossary).filter(Glossary.id == glossary_id).first()
    if not glossary_term:
        raise HTTPException(status_code=404, detail="Glossary term not found")

    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user.id,
        CartItem.glossary_id == glossary_id
    ).first()

    if existing_item:
        raise HTTPException(status_code=400, detail="Item already in cart")

    cart_item = CartItem(user_id=user.id, glossary_id=glossary_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": f"Added '{glossary_term.term}' to cart."}
