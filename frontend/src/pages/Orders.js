import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchOrders } from '../store/slices/orderSlice';
import { FiPackage, FiTruck, FiCheckCircle, FiXCircle } from 'react-icons/fi';

const Orders = () => {
  const dispatch = useDispatch();
  const { orders, isLoading } = useSelector((state) => state.orders);

  useEffect(() => {
    dispatch(fetchOrders());
  }, [dispatch]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { icon: <FiPackage />, class: 'badge-warning', text: 'Pending' },
      processing: { icon: <FiPackage />, class: 'badge-info', text: 'Processing' },
      shipped: { icon: <FiTruck />, class: 'badge-info', text: 'Shipped' },
      delivered: { icon: <FiCheckCircle />, class: 'badge-success', text: 'Delivered' },
      cancelled: { icon: <FiXCircle />, class: 'badge-error', text: 'Cancelled' },
    };

    const config = statusConfig[status] || statusConfig.pending;

    return (
      <span className={`${config.class} flex items-center space-x-1`}>
        {config.icon}
        <span>{config.text}</span>
      </span>
    );
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">My Orders</h1>

      {orders.length === 0 ? (
        <div className="text-center py-12 card">
          <FiPackage className="mx-auto text-gray-400 mb-4" size={64} />
          <h2 className="text-2xl font-bold mb-4">No orders yet</h2>
          <p className="text-gray-600 mb-8">Start shopping to create your first order!</p>
          <Link to="/products" className="btn-primary">
            Browse Products
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link
              key={order.id}
              to={`/orders/${order.id}`}
              className="card hover:shadow-lg transition block"
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div className="mb-4 md:mb-0">
                  <div className="flex items-center space-x-4 mb-2">
                    <h3 className="text-lg font-semibold">Order #{order.id}</h3>
                    {getStatusBadge(order.status)}
                  </div>
                  <p className="text-gray-600 text-sm">
                    Placed on {new Date(order.created_at).toLocaleDateString()}
                  </p>
                  <p className="text-gray-600 text-sm">
                    {order.items.length} item(s)
                  </p>
                </div>

                <div className="text-right">
                  <p className="text-2xl font-bold text-primary-600">
                    ${order.total_amount.toFixed(2)}
                  </p>
                  <button className="text-primary-600 hover:text-primary-700 font-semibold text-sm mt-2">
                    View Details →
                  </button>
                </div>
              </div>

              {/* Order Items Preview */}
              <div className="mt-4 border-t pt-4">
                <div className="flex space-x-2 overflow-x-auto">
                  {order.items.slice(0, 4).map((item) => (
                    <img
                      key={item.id}
                      src={item.product.image}
                      alt={item.product.name}
                      className="w-16 h-16 object-cover rounded"
                    />
                  ))}
                  {order.items.length > 4 && (
                    <div className="w-16 h-16 bg-gray-200 rounded flex items-center justify-center text-sm font-semibold text-gray-600">
                      +{order.items.length - 4}
                    </div>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;