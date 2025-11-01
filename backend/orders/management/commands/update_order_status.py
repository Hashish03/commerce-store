from django.core.management.base import BaseCommand
from orders.models import Order
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Auto-update order statuses based on time'
    
    def handle(self, *args, **kwargs):
        # Auto-mark orders as delivered after 7 days of shipping
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        shipped_orders = Order.objects.filter(
            status='shipped',
            shipped_at__lte=seven_days_ago
        )
        
        for order in shipped_orders:
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            
            self.stdout.write(
                f'Marked order {order.order_number} as delivered'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Updated {shipped_orders.count()} orders to delivered status'
            )
        )
