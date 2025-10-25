from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import AuditedModel


class OrderItem(AuditedModel):
    """
    Items in an order (with product snapshot).
    """
    
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Related order"
    )
    
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        help_text="Product reference"
    )
    
    # Snapshot fields (preserve product info at order time)
    product_name = models.CharField(
        max_length=200,
        help_text="Product name at order time"
    )
    
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Product price at order time"
    )
    
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity ordered"
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Subtotal (price × quantity)"
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.product_name} × {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate subtotal."""
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)

