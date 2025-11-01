from decimal import Decimal
from .models import Coupon
from django.utils import timezone

def calculate_order_total(subtotal, coupon_code=None, shipping_cost=Decimal('10.00'), tax_rate=Decimal('0.10')):
    """
    Calculate order total with tax, shipping, and discount
    """
    tax = subtotal * tax_rate
    discount = Decimal('0.00')
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(
                code=coupon_code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            
            if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                return None, "Coupon usage limit reached"
            
            if subtotal < coupon.min_purchase:
                return None, f"Minimum purchase of ${coupon.min_purchase} required"
            
            if coupon.discount_type == 'percentage':
                discount = (subtotal * coupon.discount_value) / 100
                if coupon.max_discount:
                    discount = min(discount, coupon.max_discount)
            else:
                discount = coupon.discount_value
                
        except Coupon.DoesNotExist:
            return None, "Invalid coupon code"
    
    total = subtotal + tax + shipping_cost - discount
    
    return {
        'subtotal': subtotal,
        'tax': tax,
        'shipping_cost': shipping_cost,
        'discount': discount,
        'total': total
    }, None
