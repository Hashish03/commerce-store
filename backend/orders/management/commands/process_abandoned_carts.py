from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send emails for abandoned carts'
    
    def handle(self, *args, **kwargs):
        # Find carts that haven't been updated in 24 hours
        cutoff_time = timezone.now() - timedelta(hours=24)
        abandoned_carts = Cart.objects.filter(
            updated_at__lte=cutoff_time,
            items__isnull=False
        ).distinct()
        
        for cart in abandoned_carts:
            if cart.items.count() > 0:
                self.send_abandoned_cart_email(cart)
                self.stdout.write(
                    f'Sent abandoned cart email to {cart.user.email}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Processed {abandoned_carts.count()} abandoned carts'
            )
        )
    
    def send_abandoned_cart_email(self, cart):
        subject = "Don't forget your items!"
        message = f"""
        Hi {cart.user.first_name},
        
        You left {cart.total_items} item(s) in your cart.
        Complete your purchase now!
        
        Cart Total: ${cart.subtotal}
        
        Best regards,
        Your E-commerce Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[cart.user.email],
            fail_silently=True,
        )
