from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.cart import CartItem
from ...models.order import Order, OrderItem
from ...models.otp import OTP
from ...models.user import User
from ...schemas.order import OrderResponse, CheckoutRequest
from ...schemas.otp import OTPRequest, OTPVerify
from ...dependencies import get_current_user
from ...services.email import generate_otp, send_otp_email, create_otp_record
import random

router = APIRouter(prefix="/checkout", tags=["checkout"])

@router.post("/request-otp")
def request_otp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user has items in cart
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Generate and send OTP
    otp_code = generate_otp()
    create_otp_record(db, current_user.id, otp_code)
    send_otp_email(current_user.email, otp_code)
    
    return {
        "message": "OTP sent to your email",
        "expires_in": "5 minutes"
    }

@router.post("/verify-otp")
def verify_otp_and_process_order(
    otp_data: OTPVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get the latest valid OTP for this user
    otp_record = db.query(OTP).filter(
        OTP.user_id == current_user.id,
        OTP.used == False,
        OTP.expires_at > datetime.utcnow()
    ).order_by(OTP.id.desc()).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid OTP found or OTP has expired"
        )
    
    # Check attempts limit
    if otp_record.attempts >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum OTP attempts exceeded"
        )
    
    # Increment attempts
    otp_record.attempts += 1
    
    # Verify OTP
    if otp_record.otp_code != otp_data.otp_code:
        db.commit()  # Save attempt increment
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    # Mark OTP as used
    otp_record.used = True
    
    # Get cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total amount and check stock
    total_amount = 0
    for cart_item in cart_items:
        if cart_item.product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {cart_item.product.name}"
            )
        total_amount += cart_item.product.price * cart_item.quantity
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    db.flush()  # Get order ID
    
    # Create order items and update stock
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.price
        )
        db.add(order_item)
        
        # Update product stock
        cart_item.product.stock -= cart_item.quantity
    
    # Process dummy payment (always successful for demo)
    transaction_id = f"TXN_{random.randint(100000, 999999)}"
    order.status = "paid"
    
    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    
    # Commit all changes
    db.commit()
    db.refresh(order)
    
    return {
        "order_id": order.id,
        "status": "success",
        "transaction_id": transaction_id,
        "message": "Order placed successfully"
    }
