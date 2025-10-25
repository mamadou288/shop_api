from rest_framework import serializers
from ..models import OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Serializer for creating order items (nested in order creation).
    """
    product = serializers.UUIDField(help_text="Product UUID")
    quantity = serializers.IntegerField(min_value=1, help_text="Quantity")


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying order items.
    """
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'subtotal',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'product_name',
            'product_price',
            'subtotal',
            'created_at',
        ]

