// src/components/AddGlossaryEntry.jsx
import React, { useState } from "react";
import axios from "axios";

const AddGlossaryEntry = ({ onAddSuccess }) => {
  const [form, setForm] = useState({
    term: "",
    definition: "",
    example: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.post("http://localhost:8000/glossary", form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForm({ term: "", definition: "", example: "" });
      onAddSuccess(); // Refresh glossary
    } catch (err) {
      console.error("Add failed", err);
      alert("Failed to add entry");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <input name="term" placeholder="Term" value={form.term} onChange={handleChange} required />
      <textarea name="definition" placeholder="Definition" value={form.definition} onChange={handleChange} required />
      <input name="example" placeholder="Example" value={form.example} onChange={handleChange} />
      <button type="submit">➕ Submit</button>
    </form>
  );
};

export default AddGlossaryEntry;
