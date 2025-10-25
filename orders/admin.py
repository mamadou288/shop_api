from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderStatus


class OrderItemInline(admin.TabularInline):
    """Inline for order items."""
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'subtotal']
    fields = ['product', 'product_name', 'product_price', 'quantity', 'subtotal']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for orders."""
    
    list_display = [
        'id',
        'user',
        'status_badge',
        'total_amount',
        'created_at',
        'updated_at',
    ]
    
    list_filter = [
        'status',
        'created_at',
        'updated_at',
    ]
    
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'shipping_city',
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'confirmed_at',
        'shipped_at',
        'delivered_at',
        'cancelled_at',
    ]
    
    fieldsets = (
        ('Commande', {
            'fields': ('id', 'user', 'status', 'total_amount')
        }),
        ('Livraison', {
            'fields': (
                'shipping_address',
                'shipping_city',
                'shipping_postal_code',
                'shipping_country',
                'notes',
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at',
                'confirmed_at',
                'shipped_at',
                'delivered_at',
                'cancelled_at',
            )
        }),
    )
    
    inlines = [OrderItemInline]
    
    def status_badge(self, obj):
        """Display colored status badge."""
        colors = {
            OrderStatus.PENDING: '#FFA500',      # Orange
            OrderStatus.CONFIRMED: '#4169E1',    # Royal Blue
            OrderStatus.SHIPPED: '#9370DB',      # Medium Purple
            OrderStatus.DELIVERED: '#28A745',    # Green
            OrderStatus.CANCELLED: '#DC3545',    # Red
        }
        
        color = colors.get(obj.status, '#6C757D')  # Default Gray
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    
    status_badge.short_description = 'Status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin for order items."""
    
    list_display = [
        'id',
        'order',
        'product',
        'product_name',
        'product_price',
        'quantity',
        'subtotal',
    ]
    
    list_filter = [
        'created_at',
    ]
    
    search_fields = [
        'product_name',
        'order__id',
    ]
    
    readonly_fields = [
        'id',
        'product_name',
        'product_price',
        'subtotal',
        'created_at',
        'updated_at',
    ]
