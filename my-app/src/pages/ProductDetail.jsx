import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { productsAPI, cartAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const ProductDetail = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await productsAPI.getById(id);
      setProduct(response.data);
    } catch (error) {
      console.error('Error fetching product:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      setAddingToCart(true);
      await cartAPI.add({
        product_id: parseInt(id),
        quantity: quantity,
      });
      setMessage('Product added to cart!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Error adding to cart');
      setTimeout(() => setMessage(''), 3000);
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!product) {
    return <div className="error">Product not found</div>;
  }

  return (
    <div className="product-detail">
      <div className="container">
        <div className="product-detail-content">
          <div className="product-info">
            <h1>{product.name}</h1>
            <div className="product-meta">
              <span className="category">Category: {product.category}</span>
              <span className="price">${product.price.toFixed(2)}</span>
              <span className="stock">Stock: {product.stock}</span>
            </div>
            
            {message && (
              <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
                {message}
              </div>
            )}
            
            <div className="add-to-cart-section">
              <div className="quantity-selector">
                <label htmlFor="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  min="1"
                  max={product.stock}
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                />
              </div>
              
              <button
                onClick={handleAddToCart}
                disabled={addingToCart || product.stock === 0}
                className="btn btn-primary"
              >
                {addingToCart ? 'Adding...' : 'Add to Cart'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
