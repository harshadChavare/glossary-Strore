import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { productsAPI } from '../services/api';
import './Home.css'; // Add this line

const Home = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        const response = await productsAPI.getAll();
        setFeaturedProducts(response.data.slice(0, 6));
      } catch (error) {
        console.error('Error fetching featured products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedProducts();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="home-page">
      {/* Hero Section */}
      <div className="hero">
        <div className="container">
          <h1>Welcome to Fresh Grocery Store</h1>
          <p>Get fresh groceries delivered to your door!</p>
          <Link to="/products" className="btn btn-primary">
            Shop Now
          </Link>
        </div>
      </div>

      {/* Featured Products */}
      <div className="featured-section">
        <div className="container">
          <h2>Featured Products</h2>
          <div className="products-grid">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
