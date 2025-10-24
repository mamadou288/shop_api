from django.db import models
from django.utils.text import slugify
from core.models import AuditedModel


class Category(AuditedModel):
    """
    Product categories with hierarchical support.
    
    Examples:
    - Electronics
        - Laptops
        - Phones
    - Clothing
        - Men
        - Women
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name (unique)"
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Auto-generated from name"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Category description"
    )
    
    # Hierarchy: A category can have a parent category
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent category for hierarchy"
    )
    
    # Category image (optional)
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        help_text="Category thumbnail"
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_full_path(self):
        """Get full category path: Electronics > Laptops > Gaming"""
        path = [self.name]
        parent = self.parent
        
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        
        return ' > '.join(path)

