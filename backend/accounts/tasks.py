from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_id):
    """Send welcome email to new users"""
    from accounts.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Welcome to Our Store!'
        message = f"""
        Hi {user.first_name},
        
        Welcome to our online store! We're excited to have you as a customer.
        
        Start shopping now and enjoy our wide selection of products.
        
        Best regards,
        Your E-commerce Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return f"Welcome email sent to {user.email}"
    
    except User.DoesNotExist:
        return f"User {user_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"