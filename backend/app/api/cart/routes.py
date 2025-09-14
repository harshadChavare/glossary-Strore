from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.cart import CartItem
from ...models.product import Product
from ...models.user import User
from ...schemas.cart import CartItemCreate, CartItemResponse
from ...dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=List[CartItemResponse])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return cart_items

@router.post("/", response_model=CartItemResponse)
def add_to_cart(
    cart_item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == cart_item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if product has enough stock
    if product.stock < cart_item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available"
        )
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == cart_item_data.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += cart_item_data.quantity
        if existing_item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough stock available"
            )
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Create new cart item
        new_cart_item = CartItem(
            user_id=current_user.id,
            product_id=cart_item_data.product_id,
            quantity=cart_item_data.quantity
        )
        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)
        return new_cart_item

@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock availability
    if cart_item.product.stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available"
        )
    
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.delete("/")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
