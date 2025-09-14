// src/pages/Glossary.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { getCurrentUser, isAdmin } from "../utils/auth";
import AddGlossaryEntry from "../components/AddGlossaryEntry";
import EditGlossaryEntry from "../components/EditGlossaryEntry";
import "./Glossary.css";

const Glossary = () => {
  const [entries, setEntries] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingEntryId, setEditingEntryId] = useState(null);

  const user = getCurrentUser();
  const admin = isAdmin();

  const fetchEntries = () => {
    axios
      .get("http://127.0.0.1:8000/products")
      .then((res) => {setEntries(res.data);
        // console.log(res.data,"dfrgthyujiklo;")
      })
      .catch((err) => console.error("Failed to fetch products:", err));
  };

  useEffect(() => {
    fetchEntries();
    setTimeout(() => {
    console.log('entries',entries)  
    }, 5000);
    
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/products/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setEntries(entries.filter((e) => e.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  const addToCart = async (productId) => {
    try {
      await axios.post(
        `http://127.0.0.1:8000/products/cart/add/${productId}`,
        {},
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      alert("Added to cart!");
    } catch (err) {
      console.error(err);
      alert("Failed to add to cart");
    }
  };

  const handlePurchase = async (productId) => {
    try {
      const addRes = await axios.post(
        `http://127.0.0.1:8000/products/cart/add/${productId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const cartItemId = addRes.data.id || addRes.data.cart_item_id;
      if (!cartItemId) throw new Error("No cart item ID returned");

      await axios.post(`http://127.0.0.1:8000/purchase/${cartItemId}`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      alert("🎉 Thank you for your purchase!");
      setTimeout(() => {
        window.location.href = "/glossary";
      }, 1000);
    } catch (err) {
      console.error("Direct purchase failed:", err);
      alert("❌ Purchase failed. Please try again.");
    }
  };

  const handleAddToCart = async (productId) => {
    try {
      const res = await axios.post(
        `http://127.0.0.1:8000/products/cart/add/${productId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert(res.data.message);
    } catch (err) {
      if(err.response.status===401){
        alert('Please login to add to kart')
      }
      console.error("Add to cart failed:", err);
      alert("Add to cart failed");
    }
  };

  return (
    <div className="glossary-container">
      <h1 className="glossary-title">🛍️ Products</h1>

      {admin && (
        <>
          <button onClick={() => setShowAddForm(!showAddForm)} className="add-btn">
            {showAddForm ? "➖ Hide Form" : "➕ Add New Product"}
          </button>
          {showAddForm && <AddGlossaryEntry onAddSuccess={fetchEntries} />}
        </>
      )}

      <div className="glossary-grid">
        {entries.map((entry) => (
          <div key={entry.id} className="glossary-card">
            {editingEntryId === entry.id ? (
              <EditGlossaryEntry
                entry={entry}
                onCancel={() => setEditingEntryId(null)}
                onSave={() => {
                  setEditingEntryId(null);
                  fetchEntries();
                }}
              />
            ) : (
              <>
                <h2 className="term">{entry.name}</h2>
                <p className="definition"><strong>Category:</strong> {entry.category}</p>
                <p className="definition"><strong>Price:</strong> {entry.price}</p>
                <p className="definition"><strong>Stock:</strong> {entry.stock}</p>

                {admin && (
                  <div className="admin-actions">
                    <button onClick={() => setEditingEntryId(entry.id)}>✏️ Edit</button>
                    <button onClick={() => handleDelete(entry.id)}>🗑️ Delete</button>
                  </div>
                )}

                {!admin && user && (
                  <div className="user-actions">
                    <button onClick={() => handleAddToCart(entry.id)}>🛒 Add to Cart</button>
                    <button onClick={() => handlePurchase(entry.id)}>💳 Purchase</button>
                    
                  </div>
                )}
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Glossary;
