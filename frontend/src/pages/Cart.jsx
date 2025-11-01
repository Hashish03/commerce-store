import React, { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchCart, updateCartItem, removeFromCart, clearCart } from '../store/slices/cartSlice';
import { FiTrash2, FiMinus, FiPlus, FiShoppingBag } from 'react-icons/fi';
import toast from 'react-hot-toast';

const Cart = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { items, total, isLoading } = useSelector((state) => state.cart);

  useEffect(() => {
    dispatch(fetchCart());
  }, [dispatch]);

  const handleUpdateQuantity = (itemId, currentQuantity, action) => {
    const newQuantity = action === 'increment' ? currentQuantity + 1 : currentQuantity - 1;
    
    if (newQuantity < 1) return;

    dispatch(updateCartItem({ itemId, quantity: newQuantity }))
      .unwrap()
      .catch((error) => {
        toast.error(error.message || 'Failed to update cart');
      });
  };

  const handleRemoveItem = (itemId) => {
    if (window.confirm('Are you sure you want to remove this item?')) {
      dispatch(removeFromCart(itemId))
        .unwrap()
        .then(() => {
          toast.success('Item removed from cart');
        })
        .catch((error) => {
          toast.error(error.message || 'Failed to remove item');
        });
    }
  };

  const handleClearCart = () => {
    if (window.confirm('Are you sure you want to clear your cart?')) {
      dispatch(clearCart())
        .unwrap()
        .then(() => {
          toast.success('Cart cleared successfully');
        })
        .catch((error) => {
          toast.error(error.message || 'Failed to clear cart');
        });
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <FiShoppingBag className="mx-auto text-gray-400 mb-4" size={64} />
          <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
          <p className="text-gray-600 mb-8">Add some products to get started!</p>
          <Link to="/products" className="btn-primary">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Shopping Cart</h1>
        <button
          onClick={handleClearCart}
          className="text-red-600 hover:text-red-700 font-semibold"
        >
          Clear Cart
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => (
            <div key={item.id} className="card">
              <div className="flex items-center space-x-4">
                {/* Product Image */}
                <Link to={`/products/${item.product.id}`}>
                  <img
                    src={item.product.image}
                    alt={item.product.name}
                    className="w-24 h-24 object-cover rounded-lg"
                  />
                </Link>

                {/* Product Info */}
                <div className="flex-1">
                  <Link
                    to={`/products/${item.product.id}`}
                    className="text-lg font-semibold hover:text-primary-600 transition"
                  >
                    {item.product.name}
                  </Link>
                  <p className="text-gray-600 text-sm mt-1">
                    ${item.product.price} each
                  </p>

                  {/* Quantity Controls */}
                  <div className="flex items-center space-x-3 mt-3">
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity, 'decrement')}
                      disabled={item.quantity === 1}
                      className="p-1 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50"
                    >
                      <FiMinus size={16} />
                    </button>
                    <span className="font-semibold w-8 text-center">{item.quantity}</span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity, 'increment')}
                      disabled={item.quantity >= item.product.stock}
                      className="p-1 border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50"
                    >
                      <FiPlus size={16} />
                    </button>
                  </div>
                </div>

                {/* Subtotal & Remove */}
                <div className="text-right">
                  <p className="text-xl font-bold text-primary-600 mb-2">
                    ${(item.product.price * item.quantity).toFixed(2)}
                  </p>
                  <button
                    onClick={() => handleRemoveItem(item.id)}
                    className="text-red-600 hover:text-red-700 flex items-center space-x-1"
                  >
                    <FiTrash2 />
                    <span>Remove</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="card sticky top-24">
            <h2 className="text-xl font-bold mb-4">Order Summary</h2>
            
            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span className="font-semibold">${total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Shipping</span>
                <span className="font-semibold">
                  {total >= 50 ? 'FREE' : '$10.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tax (10%)</span>
                <span className="font-semibold">${(total * 0.1).toFixed(2)}</span>
              </div>
              
              <div className="border-t pt-3">
                <div className="flex justify-between items-center">
                  <span className="text-lg font-bold">Total</span>
                  <span className="text-2xl font-bold text-primary-600">
                    ${(total + (total >= 50 ? 0 : 10) + total * 0.1).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            {total < 50 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
                <p className="text-sm text-yellow-800">
                  Add ${(50 - total).toFixed(2)} more to get free shipping!
                </p>
              </div>
            )}

            <button
              onClick={() => navigate('/checkout')}
              className="w-full btn-primary mb-3"
            >
              Proceed to Checkout
            </button>
            
            <Link
              to="/products"
              className="block text-center text-primary-600 hover:text-primary-700 font-semibold"
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;