from django.urls import path
from .views import (
    OrderListView, OrderDetailView, OrderCreateView, ValidateCouponView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
    path('coupons/validate/', ValidateCouponView.as_view(), name='validate-coupon'),
]
