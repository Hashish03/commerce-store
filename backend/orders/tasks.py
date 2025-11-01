from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email to customer"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Order Confirmation - {order.order_number}'
        
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'items': order.items.all(),
        })
        
        plain_message = f"""
        Thank you for your order!
        
        Order Number: {order.order_number}
        Total: ${order.total}
        
        We'll send you a shipping confirmation email when your order ships.
        
        Best regards,
        Your E-commerce Team
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Order confirmation email sent to {order.email}"
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"

@shared_task
def send_order_shipped_email(order_id):
    """Send shipping notification email to customer"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Your Order Has Shipped - {order.order_number}'
        
        html_message = render_to_string('emails/order_shipped.html', {
            'order': order,
            'tracking_number': order.tracking_number,
            'carrier': order.carrier,
        })
        
        plain_message = f"""
        Good news! Your order has shipped.
        
        Order Number: {order.order_number}
        Tracking Number: {order.tracking_number}
        Carrier: {order.carrier}
        
        You can track your package using the tracking number above.
        
        Best regards,
        Your E-commerce Team
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Shipping notification sent to {order.email}"
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"

@shared_task
def send_order_status_update_email(order_id, new_status):
    """Send order status update email to customer"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Order Status Update - {order.order_number}'
        
        status_messages = {
            'processing': 'Your order is being processed',
            'shipped': 'Your order has been shipped',
            'delivered': 'Your order has been delivered',
            'cancelled': 'Your order has been cancelled',
        }
        
        plain_message = f"""
        Order Status Update
        
        Order Number: {order.order_number}
        Status: {status_messages.get(new_status, new_status)}
        
        Best regards,
        Your E-commerce Team
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )
        
        return f"Status update email sent to {order.email}"
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"
