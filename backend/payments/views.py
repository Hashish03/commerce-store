from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import stripe
import json

from orders.models import Order, OrderStatusHistory

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        order_number = request.data.get('order_number')
        
        try:
            order = Order.objects.get(
                order_number=order_number,
                user=request.user,
                payment_status='pending'
            )
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'order_number': order.order_number,
                    'user_id': order.user.id,
                },
                receipt_email=order.email,
            )
            
            order.transaction_id = intent.id
            order.payment_method = 'stripe'
            order.save()
            
            return Response({
                'clientSecret': intent.client_secret,
                'publishableKey': settings.STRIPE_PUBLIC_KEY
            })
            
        except stripe.error.StripeError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PaymentSuccessView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        order_number = request.data.get('order_number')
        payment_intent_id = request.data.get('payment_intent_id')
        
        try:
            order = Order.objects.get(
                order_number=order_number,
                user=request.user
            )
            
            # Verify payment with Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                order.payment_status = 'paid'
                order.status = 'processing'
                order.paid_at = timezone.now()
                order.transaction_id = payment_intent_id
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    status='processing',
                    notes='Payment received successfully',
                    created_by=request.user
                )
                
                # TODO: Send order confirmation email
                # send_order_confirmation_email.delay(order.id)
                
                return Response({
                    'detail': 'Payment successful',
                    'order_number': order.order_number
                })
            else:
                return Response(
                    {'detail': 'Payment verification failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Order.DoesNotExist:
            return Response(
                {'detail': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except stripe.error.StripeError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = []
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_number = payment_intent['metadata'].get('order_number')
            
            try:
                order = Order.objects.get(order_number=order_number)
                if order.payment_status != 'paid':
                    order.payment_status = 'paid'
                    order.status = 'processing'
                    order.paid_at = timezone.now()
                    order.save()
                    
                    OrderStatusHistory.objects.create(
                        order=order,
                        status='processing',
                        notes='Payment confirmed via webhook'
                    )
                    
                    # TODO: Send email notification
                    # send_order_confirmation_email.delay(order.id)
                    
            except Order.DoesNotExist:
                pass
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            order_number = payment_intent['metadata'].get('order_number')
            
            try:
                order = Order.objects.get(order_number=order_number)
                order.payment_status = 'failed'
                order.save()
                
                OrderStatusHistory.objects.create(
                    order=order,
                    status='pending',
                    notes='Payment failed'
                )
                
            except Order.DoesNotExist:
                pass
        
        return HttpResponse(status=200)