import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cartAPI, checkoutAPI } from '../services/api';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [step, setStep] = useState('summary'); // 'summary', 'otp', 'payment'
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [processing, setProcessing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await cartAPI.get();
      setCartItems(response.data);
      if (response.data.length === 0) {
        navigate('/cart');
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTotalAmount = () => {
    return cartItems.reduce((total, item) => {
      return total + (item.product.price * item.quantity);
    }, 0);
  };

  const requestOTP = async () => {
    try {
      setProcessing(true);
      setError('');
      await checkoutAPI.requestOTP();
      setStep('otp');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error requesting OTP');
    } finally {
      setProcessing(false);
    }
  };

  const verifyOTPAndPay = async () => {
    try {
      setProcessing(true);
      setError('');
      const response = await checkoutAPI.verifyOTP({ otp_code: otp });
      
      // Simulate payment processing
      setTimeout(() => {
        navigate('/success', { 
          state: { 
            orderDetails: response.data,
            total: getTotalAmount()
          }
        });
      }, 2000);
      
      setStep('payment');
    } catch (error) {
      setError(error.response?.data?.detail || 'Error verifying OTP');
      setProcessing(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="checkout-page">
      <div className="container">
        <h1>Checkout</h1>
        
        {step === 'summary' && (
          <div className="checkout-summary">
            <h2>Order Summary</h2>
            
            <div className="order-items">
              {cartItems.map((item) => (
                <div key={item.id} className="order-item">
                  <span className="item-name">{item.product.name}</span>
                  <span className="item-quantity">Qty: {item.quantity}</span>
                  <span className="item-price">
                    ${(item.product.price * item.quantity).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
            
            <div className="order-total">
              <strong>Total: ${getTotalAmount().toFixed(2)}</strong>
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            <button
              onClick={requestOTP}
              disabled={processing}
              className="btn btn-primary"
            >
              {processing ? 'Requesting OTP...' : 'Request OTP to Continue'}
            </button>
          </div>
        )}

        {step === 'otp' && (
          <div className="otp-verification">
            <h2>Enter OTP</h2>
            <p>We've sent a verification code to your email. Please enter it below:</p>
            
            {error && <div className="error-message">{error}</div>}
            
            <div className="form-group">
              <input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength="6"
                className="otp-input"
              />
            </div>
            
            <div className="otp-actions">
              <button
                onClick={() => setStep('summary')}
                className="btn btn-secondary"
              >
                Back
              </button>
              <button
                onClick={verifyOTPAndPay}
                disabled={otp.length !== 6 || processing}
                className="btn btn-primary"
              >
                {processing ? 'Verifying...' : 'Verify & Pay'}
              </button>
            </div>
          </div>
        )}

        {step === 'payment' && (
          <div className="payment-processing">
            <h2>Processing Payment...</h2>
            <div className="payment-loader">
              <p>Please wait while we process your payment...</p>
              <div className="loader"></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Checkout;
