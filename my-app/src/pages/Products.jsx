import React, { useState, useEffect } from 'react';
import ProductCard from '../components/ProductCard';
import { productsAPI } from '../services/api';
import './Products.css'

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');

  const categories = ['All', 'Fruits', 'Vegetables', 'Dairy', 'Grains', 'Beverages'];

  useEffect(() => {
    fetchProducts();
  }, [category, search]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (category && category !== 'All') params.category = category;
      if (search) params.search = search;
      
      const response = await productsAPI.getAll(params);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = (selectedCategory) => {
    setCategory(selectedCategory === 'All' ? '' : selectedCategory);
  };

  return (
    <div className="products-page">
      <div className="container">
        <h1>Products</h1>
        
        <div className="filters">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="search-input"
            />
          </div>
          
          <div className="categories">
            {categories.map((cat) => (
              <button
                key={cat}
                className={`category-btn ${(cat === 'All' && !category) || cat === category ? 'active' : ''}`}
                onClick={() => handleCategoryChange(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading products...</div>
        ) : (
          <div className="products-grid">
            {products.length > 0 ? (
              products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))
            ) : (
              <div className="no-products">No products found</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;
