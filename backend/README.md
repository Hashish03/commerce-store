# E-Commerce Backend Setup

## Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis (for Celery)
- Stripe Account (for payments)

## Installation Steps

### 1. Clone the repository
git clone <your-repo-url>
cd ecommerce-store

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Setup PostgreSQL Database
# Create database
psql -U postgres
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q

### 5. Environment Configuration
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your actual credentials
nano .env

### 6. Run Migrations
python manage.py makemigrations accounts
python manage.py makemigrations products
python manage.py makemigrations cart
python manage.py makemigrations orders
python manage.py migrate

### 7. Create Superuser
python manage.py createsuperuser

### 8. Collect Static Files
python manage.py collectstatic --noinput

### 9. Load Initial Data (Optional)
# Create fixtures for categories and sample products
python manage.py loaddata initial_categories.json
python manage.py loaddata sample_products.json

### 10. Run Development Server
python manage.py runserver

### 11. Start Celery Worker (In a new terminal)
celery -A backend worker -l info

### 12. Start Celery Beat (In another terminal - for scheduled tasks)
celery -A backend beat -l info

## API Endpoints

### Authentication
- POST /api/auth/register/ - User registration
- POST /api/auth/login/ - User login
- POST /api/auth/token/refresh/ - Refresh JWT token
- GET /api/auth/profile/ - Get user profile
- PUT /api/auth/profile/ - Update user profile

### Addresses
- GET /api/auth/addresses/ - List user addresses
- POST /api/auth/addresses/ - Create address
- GET /api/auth/addresses/{id}/ - Get address detail
- PUT /api/auth/addresses/{id}/ - Update address
- DELETE /api/auth/addresses/{id}/ - Delete address

### Products
- GET /api/products/ - List products (with filters)
- GET /api/products/{slug}/ - Product detail
- GET /api/products/categories/ - List categories
- GET /api/products/{id}/reviews/ - Product reviews
- POST /api/products/{id}/reviews/ - Create review

### Wishlist
- GET /api/products/wishlist/ - Get wishlist
- POST /api/products/wishlist/ - Add to wishlist
- DELETE /api/products/wishlist/{product_id}/ - Remove from wishlist

### Cart
- GET /api/cart/ - Get cart
- POST /api/cart/add/ - Add item to cart
- PATCH /api/cart/items/{id}/ - Update cart item
- DELETE /api/cart/items/{id}/ - Remove cart item
- DELETE /api/cart/clear/ - Clear cart

### Orders
- GET /api/orders/ - List user orders
- POST /api/orders/create/ - Create order
- GET /api/orders/{order_number}/ - Order detail
- POST /api/orders/coupons/validate/ - Validate coupon

### Payments
- POST /api/payments/create-intent/ - Create payment intent
- POST /api/payments/success/ - Confirm payment
- POST /api/payments/webhook/ - Stripe webhook

## Query Parameters for Product Filtering

GET /api/products/?category=1&min_price=10&max_price=100&in_stock=true&ordering=-created_at&search=laptop

- category: Filter by category ID
- min_price: Minimum price
- max_price: Maximum price
- in_stock: Show only in-stock products (true/false)
- ordering: Sort by field (price, -price, created_at, -created_at, name)
- search: Search in product name, description, SKU

## Admin Panel
Access the Django admin at: http://localhost:8000/admin/

## Stripe Webhook Setup
1. Install Stripe CLI: https://stripe.com/docs/stripe-cli
2. Login: stripe login
3. Forward webhooks: stripe listen --forward-to localhost:8000/api/payments/webhook/
4. Copy the webhook secret to .env file

## Testing Stripe Payments
Use Stripe test cards:
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- Any future expiry date and CVC

## Production Deployment Checklist
- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Configure production database
- [ ] Setup production email backend
- [ ] Configure HTTPS
- [ ] Setup proper CORS origins
- [ ] Configure static/media file serving (AWS S3, etc.)
- [ ] Setup monitoring and logging
- [ ] Configure Celery with production broker
- [ ] Setup automated backups
- [ ] Configure rate limiting
- [ ] Review security settings

## Environment Variables Reference
See .env.example for all required environment variables.

## Support
For issues or questions, please open an issue on GitHub.