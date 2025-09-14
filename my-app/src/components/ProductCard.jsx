import React from 'react';
import { Link } from 'react-router-dom';

import './ProductCard.css';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <div className="product-header">
        <h3 className="product-name">{product.name}</h3>
        <span className="product-category">{product.category}</span>
      </div>
      
      <div className="product-details">
        <div className="product-price">${product.price.toFixed(2)}</div>
        <div className="product-stock">Stock: {product.stock}</div>
      </div>
      
      <div className="product-actions">
        <Link to={`/product/${product.id}`} className="btn btn-primary">
          View Details
        </Link>
      </div>
    </div>
  );
};

export default ProductCard;
    