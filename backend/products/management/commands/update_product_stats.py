from django.core.management.base import BaseCommand
from products.models import Product
from django.db.models import Avg, Count

class Command(BaseCommand):
    help = 'Update product statistics (ratings, review counts)'
    
    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        
        for product in products:
            reviews = product.reviews.filter(is_approved=True)
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            review_count = reviews.count()
            
            self.stdout.write(
                f'{product.name}: {review_count} reviews, {avg_rating:.1f} avg rating'
            )
        
        self.stdout.write(self.style.SUCCESS('Product statistics updated!'))
