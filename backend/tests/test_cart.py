from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Category, Product
from cart.models import Cart
from decimal import Decimal

User = get_user_model()

class CartAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
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
        
        self.client.force_authenticate(user=self.user)
    
    def test_get_empty_cart(self):
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 0)
    
    def test_add_to_cart(self):
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post('/api/cart/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_items'], 2)
    
    def test_add_to_cart_exceeds_stock(self):
        data = {
            'product_id': self.product.id,
            'quantity': 20
        }
        response = self.client.post('/api/cart/add/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

