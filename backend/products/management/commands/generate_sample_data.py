from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate sample data for testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and gear'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample products
        products_data = [
            {
                'name': 'Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'short_description': 'Premium wireless headphones',
                'price': Decimal('99.99'),
                'compare_price': Decimal('149.99'),
                'stock': 50,
                'category': categories[0],
            },
            {
                'name': 'Smartphone Stand',
                'description': 'Adjustable smartphone stand for desk',
                'short_description': 'Adjustable phone stand',
                'price': Decimal('19.99'),
                'stock': 100,
                'category': categories[0],
            },
            {
                'name': 'Cotton T-Shirt',
                'description': '100% cotton comfortable t-shirt',
                'short_description': 'Comfortable cotton tee',
                'price': Decimal('24.99'),
                'stock': 200,
                'category': categories[1],
            },
            {
                'name': 'Python Programming Book',
                'description': 'Learn Python programming from scratch',
                'short_description': 'Python learning guide',
                'price': Decimal('39.99'),
                'stock': 75,
                'category': categories[2],
            },
            {
                'name': 'Garden Tool Set',
                'description': 'Complete garden tool set with storage bag',
                'short_description': 'Essential garden tools',
                'price': Decimal('79.99'),
                'stock': 30,
                'category': categories[3],
            },
            {
                'name': 'Yoga Mat',
                'description': 'Non-slip yoga mat with carrying strap',
                'short_description': 'Premium yoga mat',
                'price': Decimal('29.99'),
                'stock': 150,
                'category': categories[4],
            },
        ]
        
        for i, prod_data in enumerate(products_data):
            product, created = Product.objects.get_or_create(
                sku=f'PROD{str(i+1).zfill(5)}',
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data generated successfully!'))
