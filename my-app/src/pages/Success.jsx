import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Success = () => {
  const location = useLocation();
  const { orderDetails, total } = location.state || {};

  return (
    <div className="success-page">
      <div className="container">
        <div className="success-content">
          <div className="success-icon">✅</div>
          <h1>Order Placed Successfully!</h1>
          
          {orderDetails && (
            <div className="order-details">
              <h2>Order Details</h2>
              <div className="detail-item">
                <strong>Order ID:</strong> {orderDetails.order_id}
              </div>
              <div className="detail-item">
                <strong>Transaction ID:</strong> {orderDetails.transaction_id}
              </div>
              <div className="detail-item">
                <strong>Status:</strong> {orderDetails.status}
              </div>
              {total && (
                <div className="detail-item">
                  <strong>Total Amount:</strong> ${total.toFixed(2)}
                </div>
              )}
            </div>
          )}
          
          <div className="success-actions">
            <Link to="/" className="btn btn-primary">
              Back to Home
            </Link>
            <Link to="/products" className="btn btn-secondary">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Success;
