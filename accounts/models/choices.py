from django.db import models


class LanguageChoices(models.TextChoices):
    """Language choices for user preferences."""
    FRENCH = 'fr', 'Français'
    ENGLISH = 'en', 'English'


class CurrencyChoices(models.TextChoices):
    """Currency choices for user preferences."""
    EURO = 'EUR', 'Euro'
    DOLLAR = 'USD', 'Dollar'

