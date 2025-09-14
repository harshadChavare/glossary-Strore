import axios from 'axios';

// const API_BASE_URL = 'http://localhost:8000/api';
const API_BASE_URL = 'https://glossary-strore.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
};

// Products API
export const productsAPI = {
  getAll: (params = {}) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}`),
  create: (productData) => api.post('/products/', productData),
  update: (id, productData) => api.put(`/products/${id}`, productData),
  delete: (id) => api.delete(`/products/${id}`),
};

// Cart API
export const cartAPI = {
  get: () => api.get('/cart/'),
  add: (item) => api.post('/cart/', item),
  update: (id, quantity) => api.put(`/cart/${id}?quantity=${quantity}`),
  remove: (id) => api.delete(`/cart/${id}`),
  clear: () => api.delete('/cart/'),
};

// Checkout API
export const checkoutAPI = {
  requestOTP: () => api.post('/checkout/request-otp'),
  verifyOTP: (otpData) => api.post('/checkout/verify-otp', otpData),
};

// Admin API
export const adminAPI = {
  getProducts: () => api.get('/admin/products'),
  getOrders: () => api.get('/admin/orders'),
  getUsers: () => api.get('/admin/users'),
};

export default api;
