from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import GlossaryCreate, GlossaryOut
from auth import get_current_user, get_current_admin_user
from database import get_db
from models import CartItem, Glossary

router = APIRouter()

@router.get("/glossary", response_model=List[GlossaryOut])
def get_glossary_entries(db: Session = Depends(get_db)):
    return db.query(Glossary).all()

@router.post("/glossary", response_model=GlossaryOut)
def create_glossary_entry(entry: GlossaryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Everyone logged in can add a glossary entry
    glossary_entry = Glossary(**entry.dict(), user_id=user.id)
    db.add(glossary_entry)
    db.commit()
    db.refresh(glossary_entry)
    return glossary_entry

@router.put("/glossary/{entry_id}", response_model=GlossaryOut)
def update_glossary_entry(entry_id: int, entry: GlossaryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    glossary_entry = db.query(Glossary).filter(Glossary.id == entry_id).first()
    if not glossary_entry:
        raise HTTPException(status_code=404, detail="Glossary entry not found")

    # Admin can edit any, user can only edit own
    if user.role != "admin" and glossary_entry.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this entry")

    for key, value in entry.dict().items():
        setattr(glossary_entry, key, value)

    db.commit()
    db.refresh(glossary_entry)
    return glossary_entry

@router.delete("/glossary/{entry_id}")
def delete_glossary_entry(entry_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    glossary_entry = db.query(Glossary).filter(Glossary.id == entry_id).first()
    if not glossary_entry:
        raise HTTPException(status_code=404, detail="Glossary entry not found")

    # Admin can delete any, user can only delete own
    if user.role != "admin" and glossary_entry.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this entry")

    db.delete(glossary_entry)
    db.commit()
    return {"message": f"Glossary entry '{glossary_entry.term}' deleted"}


@router.post("/cart/add/{glossary_id}")
def add_to_cart(glossary_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user.id,
        CartItem.glossary_id == glossary_id
    ).first()

    if existing_item:
        return {"message": "Already in cart", "id": existing_item.id}

    cart_item = CartItem(user_id=user.id, glossary_id=glossary_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {"message": "Added to cart", "id": cart_item.id}


@router.get("/cart")
def get_cart_items(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return [{"id": item.id, "term": item.glossary.term, "definition": item.glossary.definition} for item in items]

@router.delete("/cart/remove/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete(item)
    db.commit()
    return {"message": "Removed from cart"}

@router.post("/cart/purchase")
def purchase_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    # Dummy purchase logic: just clear the cart
    for item in items:
        db.delete(item)
    db.commit()
    return {"message": "Purchase successful!"}


@router.post("/purchase/{item_id}")
def purchase_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        # ✅ Use CartItem model instead of cart_items
        cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()

        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        # Simulate purchase
        db.delete(cart_item)
        db.commit()
        return {"message": "Purchase successful"}

    except Exception as e:
        print(f"Purchase error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


