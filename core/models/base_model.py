import uuid
from django.db import models


class AuditedModel(models.Model):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier (UUID)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Soft delete flag - False means deleted"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def soft_delete(self):
        """Soft delete the record by setting is_active to False."""
        self.is_active = False
        self.save()
    
    def restore(self):
        """Restore a soft deleted record."""
        self.is_active = True
        self.save()

