from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from core.models import AuditedModel
from .choices import OrderStatus


class Order(AuditedModel):
    """
    Customer orders.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
        help_text="Customer who placed the order"
    )
    
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        help_text="Order status"
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total order amount"
    )
    
    # Shipping information
    shipping_address = models.TextField(
        help_text="Delivery address"
    )
    
    shipping_city = models.CharField(
        max_length=100,
        help_text="City"
    )
    
    shipping_postal_code = models.CharField(
        max_length=20,
        help_text="Postal code"
    )
    
    shipping_country = models.CharField(
        max_length=100,
        default='France',
        help_text="Country"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    
    # Status timestamps
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When order was confirmed"
    )
    
    shipped_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When order was shipped"
    )
    
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When order was delivered"
    )
    
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When order was cancelled"
    )
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.user.email} - {self.status}"
    
    def calculate_total(self):
        """Calculate total from order items."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount', 'updated_at'])
    
    def can_be_cancelled(self):
        """Check if order can be cancelled."""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def cancel(self):
        """Cancel order and restore stock."""
        if not self.can_be_cancelled():
            raise ValueError(f"Cannot cancel order with status {self.status}")
        
        # Restore stock for each item
        for item in self.items.all():
            item.product.increase_stock(item.quantity)
        
        # Update status
        self.status = OrderStatus.CANCELLED
        self.cancelled_at = timezone.now()
        self.save(update_fields=['status', 'cancelled_at', 'updated_at'])
    
    def confirm(self):
        """Confirm order."""
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot confirm order with status {self.status}")
        
        self.status = OrderStatus.CONFIRMED
        self.confirmed_at = timezone.now()
        self.save(update_fields=['status', 'confirmed_at', 'updated_at'])
    
    def ship(self):
        """Mark order as shipped."""
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError(f"Cannot ship order with status {self.status}")
        
        self.status = OrderStatus.SHIPPED
        self.shipped_at = timezone.now()
        self.save(update_fields=['status', 'shipped_at', 'updated_at'])
    
    def deliver(self):
        """Mark order as delivered."""
        if self.status != OrderStatus.SHIPPED:
            raise ValueError(f"Cannot deliver order with status {self.status}")
        
        self.status = OrderStatus.DELIVERED
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at', 'updated_at'])

