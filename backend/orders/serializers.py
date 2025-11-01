from rest_framework import serializers
from orders.models import Order, OrderItem, OrderStatusHistory, Coupon
from accounts.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['status', 'notes', 'created_at']

class OrderListSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'payment_status', 'total', 
                  'item_count', 'created_at']
    
    def get_item_count(self, obj):
        return obj.items.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    billing_address = AddressSerializer(read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'payment_status', 'subtotal', 
                  'tax', 'shipping_cost', 'discount', 'total', 'shipping_address',
                  'billing_address', 'email', 'phone', 'customer_notes', 'items',
                  'tracking_number', 'carrier', 'status_history', 'created_at',
                  'paid_at', 'shipped_at', 'delivered_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    shipping_address_id = serializers.IntegerField(write_only=True)
    billing_address_id = serializers.IntegerField(write_only=True)
    coupon_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Order
        fields = ['shipping_address_id', 'billing_address_id', 'email', 
                  'phone', 'customer_notes', 'coupon_code']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'description', 'discount_type', 'discount_value', 
                  'min_purchase', 'valid_from', 'valid_to']