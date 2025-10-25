from django.db import models


class OrderStatus(models.TextChoices):
    """
    Order status choices.
    """
    PENDING = 'pending', 'En attente'
    CONFIRMED = 'confirmed', 'Confirmée'
    SHIPPED = 'shipped', 'Expédiée'
    DELIVERED = 'delivered', 'Livrée'
    CANCELLED = 'cancelled', 'Annulée'

