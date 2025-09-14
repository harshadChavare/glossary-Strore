// src/components/EditGlossaryEntry.jsx
import React, { useState } from "react";
import axios from "axios";

const EditGlossaryEntry = ({ entry, onCancel, onSave }) => {
  const [form, setForm] = useState({
    name: entry.name,
    category: entry.category,
    price: entry.price,
    stock: entry.stock,
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.put(`http://127.0.0.1:8000/products/${entry.id}`, form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      onSave();
    } catch (err) {
      console.error("Edit failed", err);
      alert("Update failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="edit-form">
      <input name="name" value={form.name} onChange={handleChange} required />
      <input name="category" value={form.category} onChange={handleChange} required />
      <input name="price" type="number" value={form.price} onChange={handleChange} required />
      <input name="stock" type="number" value={form.stock} onChange={handleChange} required />
      <button type="submit">💾 Save</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: "1rem" }}>
        ❌ Cancel
      </button>
    </form>
  );
};

export default EditGlossaryEntry;
