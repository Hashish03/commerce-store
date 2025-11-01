from django.urls import path
from .views import (
    CreatePaymentIntentView, PaymentSuccessView, StripeWebhookView
)

urlpatterns = [
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]