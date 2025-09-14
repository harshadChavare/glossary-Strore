import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { cartAPI } from '../services/api';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await cartAPI.get();
      setCartItems(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    try {
      setUpdating({ ...updating, [itemId]: true });
      await cartAPI.update(itemId, newQuantity);
      await fetchCart();
    } catch (error) {
      console.error('Error updating cart:', error);
    } finally {
      setUpdating({ ...updating, [itemId]: false });
    }
  };

  const removeItem = async (itemId) => {
    try {
      await cartAPI.remove(itemId);
      await fetchCart();
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };

  const getTotalAmount = () => {
    return cartItems.reduce((total, item) => {
      return total + (item.product.price * item.quantity);
    }, 0);
  };

  if (loading) {
    return <div className="loading">Loading cart...</div>;
  }

  return (
    <div className="cart-page">
      <div className="container">
        <h1>Shopping Cart</h1>
        
        {cartItems.length === 0 ? (
          <div className="empty-cart">
            <p>Your cart is empty</p>
            <Link to="/products" className="btn btn-primary">
              Continue Shopping
            </Link>
          </div>
        ) : (
          <>
            <div className="cart-items">
              {cartItems.map((item) => (
                <div key={item.id} className="cart-item">
                  <div className="item-info">
                    <h3>{item.product.name}</h3>
                    <p className="category">{item.product.category}</p>
                    <p className="price">${item.product.price.toFixed(2)} each</p>
                  </div>
                  
                  <div className="quantity-controls">
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      disabled={updating[item.id]}
                      className="qty-btn"
                    >
                      -
                    </button>
                    <span className="quantity">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      disabled={updating[item.id]}
                      className="qty-btn"
                    >
                      +
                    </button>
                  </div>
                  
                  <div className="item-total">
                    ${(item.product.price * item.quantity).toFixed(2)}
                  </div>
                  
                  <button
                    onClick={() => removeItem(item.id)}
                    className="remove-btn"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
            
            <div className="cart-summary">
              <div className="total">
                <strong>Total: ${getTotalAmount().toFixed(2)}</strong>
              </div>
              <div className="checkout-actions">
                <Link to="/products" className="btn btn-secondary">
                  Continue Shopping
                </Link>
                <button
                  onClick={() => navigate('/checkout')}
                  className="btn btn-primary"
                >
                  Proceed to Checkout
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
