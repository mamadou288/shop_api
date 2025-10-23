from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'is_admin', 'is_staff', 'is_active', 'created_at'
    ]
    
    list_filter = ['is_admin', 'is_staff', 'is_active', 'created_at']
    
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'phone', 'is_admin', 'newsletter_consent',
                'marketing_consent', 'date_of_birth', 'language', 'currency'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
