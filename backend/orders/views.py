from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import Order, OrderItem, OrderStatusHistory, Coupon
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, 
    OrderCreateSerializer, CouponSerializer
)
from cart.models import Cart
from accounts.models import Address

class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items', 'status_history'
        )

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cart.items.exists():
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get addresses
        shipping_address = get_object_or_404(
            Address, 
            id=serializer.validated_data['shipping_address_id'],
            user=request.user
        )
        billing_address = get_object_or_404(
            Address,
            id=serializer.validated_data['billing_address_id'],
            user=request.user
        )
        
        # Calculate totals
        subtotal = cart.subtotal
        tax = subtotal * 0.1  # 10% tax rate
        shipping_cost = 10.00  # Fixed shipping cost
        discount = 0
        
        # Apply coupon if provided
        coupon_code = serializer.validated_data.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code,
                    is_active=True,
                    valid_from__lte=timezone.now(),
                    valid_to__gte=timezone.now()
                )
                
                if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                    return Response(
                        {'detail': 'Coupon usage limit reached'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if subtotal < coupon.min_purchase:
                    return Response(
                        {'detail': f'Minimum purchase of ${coupon.min_purchase} required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if coupon.discount_type == 'percentage':
                    discount = (subtotal * coupon.discount_value) / 100
                    if coupon.max_discount:
                        discount = min(discount, coupon.max_discount)
                else:
                    discount = coupon.discount_value
                
                coupon.used_count += 1
                coupon.save()
                
            except Coupon.DoesNotExist:
                return Response(
                    {'detail': 'Invalid coupon code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        total = subtotal + tax + shipping_cost - discount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            email=serializer.validated_data.get('email', request.user.email),
            phone=serializer.validated_data.get('phone', request.user.phone),
            shipping_address=shipping_address,
            billing_address=billing_address,
            customer_notes=serializer.validated_data.get('customer_notes', ''),
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping_cost,
            discount=discount,
            total=total
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_sku=cart_item.variant.sku if cart_item.variant else cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price
            )
            
            # Reduce stock
            if cart_item.variant:
                cart_item.variant.stock -= cart_item.quantity
                cart_item.variant.save()
            else:
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order created',
            created_by=request.user
        )
        
        # Clear cart
        cart.items.all().delete()
        
        # Return order details
        response_serializer = OrderDetailSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class ValidateCouponView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'detail': 'Coupon code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            coupon = Coupon.objects.get(
                code=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            
            if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                return Response(
                    {'detail': 'Coupon usage limit reached'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = CouponSerializer(coupon)
            return Response(serializer.data)
            
        except Coupon.DoesNotExist:
            return Response(
                {'detail': 'Invalid or expired coupon code'},
                status=status.HTTP_404_NOT_FOUND
            )

