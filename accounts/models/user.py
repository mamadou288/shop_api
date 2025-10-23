import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import LanguageChoices, CurrencyChoices


class User(AbstractUser):
    """
    Custom User model with email as username field.
    
    - Email login
    - Phone number
    - Admin permissions
    - GDPR consents
    - Internationalization (language, currency)
    - Personalization (date of birth)
    """
    
    # Override id to use UUID
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Email as login field
    email = models.EmailField(
        unique=True,
        help_text="Email address for login and notifications"
    )
    
    # Contact information
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    
    # Business permissions
    is_admin = models.BooleanField(
        default=False,
        help_text="Admin can manage products and orders"
    )
    
    # GDPR 
    newsletter_consent = models.BooleanField(
        default=False,
        help_text="User consented to receive newsletter"
    )
    
    marketing_consent = models.BooleanField(
        default=False,
        help_text="User consented to receive marketing communications"
    )
    
    # Personalization
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth for analytics and birthday promotions"
    )
    
    # Internationalization
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        default=LanguageChoices.FRENCH,
        help_text="Preferred language"
    )
    
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.EURO,
        help_text="Preferred currency"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return first_name + last_name."""
        return f"{self.first_name} {self.last_name}".strip()

