import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { addToCart } from '../../store/slices/cartSlice';
import { FiShoppingCart, FiStar } from 'react-icons/fi';
import toast from 'react-hot-toast';

const ProductCard = ({ product }) => {
  const dispatch = useDispatch();
  const { isAuthenticated } = useSelector((state) => state.auth);

  const handleAddToCart = (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      toast.error('Please login to add items to cart');
      return;
    }

    if (product.stock === 0) {
      toast.error('Product out of stock');
      return;
    }

    dispatch(addToCart({ productId: product.id, quantity: 1 }))
      .unwrap()
      .then(() => {
        toast.success('Added to cart successfully!');
      })
      .catch((error) => {
        toast.error(error.message || 'Failed to add to cart');
      });
  };

  return (
    <Link to={`/products/${product.id}`} className="group">
      <div className="card hover:shadow-xl transition-all duration-300">
        {/* Product Image */}
        <div className="relative overflow-hidden rounded-lg mb-4 h-48 bg-gray-200">
          {product.image ? (
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              No Image
            </div>
          )}
          
          {/* Stock Badge */}
          {product.stock === 0 && (
            <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-xs font-semibold">
              Out of Stock
            </div>
          )}
          
          {/* Discount Badge */}
          {product.discount > 0 && (
            <div className="absolute top-2 left-2 bg-green-500 text-white px-2 py-1 rounded text-xs font-semibold">
              -{product.discount}%
            </div>
          )}
        </div>

        {/* Product Info */}
        <div>
          <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2 group-hover:text-primary-600 transition">
            {product.name}
          </h3>
          
          {/* Rating */}
          <div className="flex items-center mb-2">
            <div className="flex items-center text-yellow-400">
              <FiStar fill="currentColor" size={16} />
              <span className="ml-1 text-sm text-gray-600">
                {product.average_rating?.toFixed(1) || '0.0'} ({product.review_count || 0})
              </span>
            </div>
          </div>

          {/* Price */}
          <div className="flex items-center justify-between mb-3">
            <div>
              <span className="text-xl font-bold text-primary-600">
                ${product.price}
              </span>
              {product.original_price && product.original_price > product.price && (
                <span className="ml-2 text-sm text-gray-500 line-through">
                  ${product.original_price}
                </span>
              )}
            </div>
          </div>

          {/* Add to Cart Button */}
          <button
            onClick={handleAddToCart}
            disabled={product.stock === 0}
            className="w-full btn-primary flex items-center justify-center space-x-2"
          >
            <FiShoppingCart />
            <span>{product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}</span>
          </button>
        </div>
      </div>
    </Link>
  );
};

export default ProductCard;