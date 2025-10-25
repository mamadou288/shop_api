from django.db import models
from core.models import AuditedModel


class ProductImage(AuditedModel):
    """
    Product images (multiple per product).
    """
    
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Related product"
    )
    
    image = models.ImageField(
        upload_to='products/%Y/%m/',
        help_text="Product image"
    )
    
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Image alt text for accessibility"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (0 = first)"
    )
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['product', 'order']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
    
    def save(self, *args, **kwargs):
        """Auto-generate alt_text from product name"""
        if not self.alt_text:
            self.alt_text = f"{self.product.name} - Image"
        super().save(*args, **kwargs)

