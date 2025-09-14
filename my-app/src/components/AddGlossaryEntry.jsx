// src/components/AddGlossaryEntry.jsx
import React, { useState } from "react";
import axios from "axios";

const AddGlossaryEntry = ({ onAddSuccess }) => {
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    stock: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.post("http://127.0.0.1:8000/products", form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForm({ name: "", category: "", price: "", stock: "" });
      onAddSuccess();
    } catch (err) {
      console.error("Add failed", err);
      alert("Failed to add product");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <input name="name" placeholder="Product Name" value={form.name} onChange={handleChange} required />
      <input name="category" placeholder="Category" value={form.category} onChange={handleChange} required />
      <input name="price" type="number" placeholder="Price" value={form.price} onChange={handleChange} required />
      <input name="stock" type="number" placeholder="Stock" value={form.stock} onChange={handleChange} required />
      <button type="submit">➕ Submit</button>
    </form>
  );
};

export default AddGlossaryEntry;
