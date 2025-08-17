// src/utils/auth.js
import { jwtDecode } from "jwt-decode";

export function getCurrentUser() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const decoded = jwtDecode(token);
    return decoded?.sub || null; // Assuming `sub` contains email/username
  } catch (error) {
    console.error("Invalid token:", error);
    return null;
  }
}

export function isAdmin() {
  const user = getCurrentUser();
  return user === "admin@gmail.com";
}
