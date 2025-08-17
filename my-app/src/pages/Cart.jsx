// src/pages/Cart.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  const fetchCart = async () => {
    try {
      const res = await axios.get("http://localhost:8000/cart", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setCartItems(res.data);
    } catch (err) {
      console.error("Failed to fetch cart:", err);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const handlePurchase = async (id) => {
    try {
      await axios.post(`http://localhost:8000/purchase/${id}`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      alert("Payment successful!");
      fetchCart(); // refresh cart
    } catch (err) {
      console.error("Payment failed:", err);
    }
  };

  const handleRemove = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/cart/remove/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      fetchCart(); // refresh cart
    } catch (err) {
      console.error("Remove failed:", err);
    }
  };

  return (
    <div>
      <h2>🛒 Your Cart</h2>
      {cartItems.length === 0 ? (
        <p>No items in cart.</p>
      ) : (
        <ul>
  {cartItems.map((item) => (
    <li key={item.id}>
      <strong>{item.term}</strong> - {item.definition}
      <br />
      <button onClick={() => handlePurchase(item.id)}>💳 Purchase</button>
      <button onClick={() => handleRemove(item.id)}>❌ Remove</button>
    </li>
  ))}
</ul>

      )}
    </div>
  );
};

export default Cart;
