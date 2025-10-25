from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404
from ..models import Order, OrderItem
from products.models import Product
from .order_item import OrderItemCreateSerializer, OrderItemSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders with nested items.
    Validates stock and creates order items automatically.
    """
    items = OrderItemCreateSerializer(many=True, help_text="Order items")
    
    class Meta:
        model = Order
        fields = [
            'id',
            'items',
            'shipping_address',
            'shipping_city',
            'shipping_postal_code',
            'shipping_country',
            'notes',
        ]
    
    def validate_items(self, items):
        """Validate that items list is not empty."""
        if not items:
            raise serializers.ValidationError("Au moins un article est requis.")
        return items
    
    @transaction.atomic
    def create(self, validated_data):
        """Create order with items and reduce stock."""
        items_data = validated_data.pop('items')
        
        # Create order
        order = Order.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        # Process each item
        for item_data in items_data:
            product_id = item_data['product']
            quantity = item_data['quantity']
            
            # Get product
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            # Validate stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Stock insuffisant pour {product.name}. "
                    f"Disponible : {product.stock}, Demandé : {quantity}"
                )
            
            # Create order item with snapshot
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_price=product.price,
                quantity=quantity,
            )
            
            # Reduce stock
            product.reduce_stock(quantity)
        
        # Calculate total
        order.calculate_total()
        
        return order


class OrderSerializer(serializers.ModelSerializer):
    """
    Detailed order serializer with nested items.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_email',
            'status',
            'status_display',
            'total_amount',
            'shipping_address',
            'shipping_city',
            'shipping_postal_code',
            'shipping_country',
            'notes',
            'items',
            'created_at',
            'updated_at',
            'confirmed_at',
            'shipped_at',
            'delivered_at',
            'cancelled_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'user_email',
            'status',
            'status_display',
            'total_amount',
            'items',
            'created_at',
            'updated_at',
            'confirmed_at',
            'shipped_at',
            'delivered_at',
            'cancelled_at',
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for order list.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user_email',
            'status',
            'status_display',
            'total_amount',
            'items_count',
            'shipping_city',
            'created_at',
        ]
        read_only_fields = fields

