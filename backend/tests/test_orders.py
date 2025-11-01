from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Category, Product
from accounts.models import Address
from cart.models import Cart, CartItem
from decimal import Decimal

User = get_user_model()

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.address = Address.objects.create(
            user=self.user,
            address_type='shipping',
            street_address='123 Test St',
            city='Test City',
            state='TS',
            postal_code='12345',
            country='USA'
        )
        
        category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test',
            category=category,
            price=Decimal('50.00'),
            sku='TEST001',
            stock=10
        )
        
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        
        self.client.force_authenticate(user=self.user)
    
    def test_create_order(self):
        data = {
            'shipping_address_id': self.address.id,
            'billing_address_id': self.address.id,
            'email': 'test@example.com',
            'phone': '1234567890'
        }
        response = self.client.post('/api/orders/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_number', response.data)
    
    def test_list_user_orders(self):
        # Create an order first
        data = {
            'shipping_address_id': self.address.id,
            'billing_address_id': self.address.id,
            'email': 'test@example.com'
        }
        self.client.post('/api/orders/create/', data)
        
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

