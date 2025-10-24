from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import AuditedModel


class Product(AuditedModel):
    """
    Products available for purchase.
    """
    
    name = models.CharField(
        max_length=200,
        help_text="Product name"
    )
    
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        help_text="Auto-generated URL-friendly name"
    )
    
    description = models.TextField(
        help_text="Detailed product description"
    )
    
    # Price and stock
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Product price (min 0.01)"
    )
    
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Available quantity"
    )
    
    # Category
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,  # Don't delete if products exist
        related_name='products',
        help_text="Product category"
    )
    
    # SKU (Stock Keeping Unit)
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique product identifier"
    )
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        """Check if product is available"""
        return self.stock > 0 and self.is_active
    
    def reduce_stock(self, quantity):
        """Reduce stock (use in orders)"""
        if quantity > self.stock:
            raise ValueError(f"Insufficient stock. Available: {self.stock}")
        
        self.stock -= quantity
        self.save(update_fields=['stock', 'updated_at'])
    
    def increase_stock(self, quantity):
        """Increase stock (use in refunds)"""
        self.stock += quantity
        self.save(update_fields=['stock', 'updated_at'])

