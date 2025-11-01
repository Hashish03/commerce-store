import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchOrderById } from '../store/slices/orderSlice';
import { FiPackage, FiTruck, FiCheckCircle, FiMapPin } from 'react-icons/fi';

const OrderDetail = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { order, isLoading } = useSelector((state) => state.orders);

  useEffect(() => {
    dispatch(fetchOrderById(id));
  }, [dispatch, id]);

  const getStatusInfo = (status) => {
    const statusConfig = {
      pending: { color: 'yellow', text: 'Order Pending', icon: <FiPackage size={24} /> },
      processing: { color: 'blue', text: 'Processing', icon: <FiPackage size={24} /> },
      shipped: { color: 'blue', text: 'Shipped', icon: <FiTruck size={24} /> },
      delivered: { color: 'green', text: 'Delivered', icon: <FiCheckCircle size={24} /> },
      cancelled: { color: 'red', text: 'Cancelled', icon: <FiPackage size={24} /> },
    };

    return statusConfig[status] || statusConfig.pending;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
        <h2 className="text-2xl font-bold mb-4">Order not found</h2>
        <button onClick={() => navigate('/orders')} className="btn-primary">
          Back to Orders
        </button>
      </div>
    );
  }

  const statusInfo = getStatusInfo(order.status);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/orders')}
          className="text-primary-600 hover:text-primary-700 mb-4"
        >
          ← Back to Orders
        </button>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Order #{order.id}</h1>
            <p className="text-gray-600">
              Placed on {new Date(order.created_at).toLocaleDateString()} at{' '}
              {new Date(order.created_at).toLocaleTimeString()}
            </p>
          </div>
          <div className={`badge-${statusInfo.color === 'yellow' ? 'warning' : statusInfo.color === 'green' ? 'success' : statusInfo.color === 'red' ? 'error' : 'info'}`}>
            {statusInfo.text}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Order Items & Timeline */}
        <div className="lg:col-span-2 space-y-6">
          {/* Order Timeline */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Order Status</h2>
            <div className="space-y-4">
              {['pending', 'processing', 'shipped', 'delivered'].map((status, index) => {
                const isCompleted = ['pending', 'processing', 'shipped', 'delivered'].indexOf(order.status) >= index;
                const isCurrent = order.status === status;
                
                return (
                  <div key={status} className="flex items-center">
                    <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                      isCompleted ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-400'
                    } ${isCurrent ? 'ring-4 ring-primary-200' : ''}`}>
                      {getStatusInfo(status).icon}
                    </div>
                    <div className="ml-4 flex-1">
                      <p className={`font-semibold ${isCompleted ? 'text-gray-900' : 'text-gray-400'}`}>
                        {getStatusInfo(status).text}
                      </p>
                      {status === 'pending' && order.created_at && (
                        <p className="text-sm text-gray-500">
                          {new Date(order.created_at).toLocaleString()}
                        </p>
                      )}
                      {status === 'delivered' && order.delivered_at && (
                        <p className="text-sm text-gray-500">
                          {new Date(order.delivered_at).toLocaleString()}
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Order Items */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Order Items</h2>
            <div className="space-y-4">
              {order.items.map((item) => (
                <div key={item.id} className="flex items-center space-x-4 pb-4 border-b last:border-b-0">
                  <img
                    src={item.product.image}
                    alt={item.product.name}
                    className="w-20 h-20 object-cover rounded-lg"
                  />
                  <div className="flex-1">
                    <h3 className="font-semibold">{item.product.name}</h3>
                    <p className="text-gray-600 text-sm">Quantity: {item.quantity}</p>
                    <p className="text-gray-600 text-sm">${item.price} each</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-primary-600">
                      ${(item.price * item.quantity).toFixed(2)}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Order Summary */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Order Summary</h2>
            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal</span>
                <span>${(order.total_amount - order.shipping_cost - order.tax_amount).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Shipping</span>
                <span>${order.shipping_cost?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Tax</span>
                <span>${order.tax_amount?.toFixed(2) || '0.00'}</span>
              </div>
              {order.discount_amount > 0 && (
                <div className="flex justify-between text-sm text-green-600">
                  <span>Discount</span>
                  <span>-${order.discount_amount.toFixed(2)}</span>
                </div>
              )}
            </div>
            <div className="border-t pt-4">
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold">Total</span>
                <span className="text-2xl font-bold text-primary-600">
                  ${order.total_amount.toFixed(2)}
                </span>
              </div>
            </div>
          </div>

          {/* Shipping Address */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <FiMapPin className="mr-2" />
              Shipping Address
            </h2>
            <div className="text-gray-600">
              <p>{order.shipping_address?.address_line1}</p>
              {order.shipping_address?.address_line2 && (
                <p>{order.shipping_address.address_line2}</p>
              )}
              <p>
                {order.shipping_address?.city}, {order.shipping_address?.state}{' '}
                {order.shipping_address?.zip_code}
              </p>
              <p>{order.shipping_address?.country}</p>
            </div>
          </div>

          {/* Payment Information */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Payment Information</h2>
            <div className="text-gray-600">
              <p className="mb-2">
                <span className="font-semibold">Payment Method:</span> Card
              </p>
              <p>
                <span className="font-semibold">Transaction ID:</span>{' '}
                {order.payment_intent_id || 'N/A'}
              </p>
            </div>
          </div>

          {/* Actions */}
          {order.status !== 'cancelled' && order.status !== 'delivered' && (
            <div className="card">
              <button className="w-full btn-outline text-red-600 border-red-600 hover:bg-red-50">
                Cancel Order
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;