// src/components/EditGlossaryEntry.jsx
import React, { useState } from "react";
import axios from "axios";

const EditGlossaryEntry = ({ entry, onCancel, onSave }) => {
  const [form, setForm] = useState({
    term: entry.term,
    definition: entry.definition,
    example: entry.example || "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.put(`https://glossary-strore.onrender.com/glossary/${entry.id}`, form, {
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
      <input name="term" value={form.term} onChange={handleChange} required />
      <textarea name="definition" value={form.definition} onChange={handleChange} required />
      <input name="example" value={form.example} onChange={handleChange} />
      <button type="submit">💾 Save</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: "1rem" }}>
        ❌ Cancel
      </button>
    </form>
  );
};

export default EditGlossaryEntry;
