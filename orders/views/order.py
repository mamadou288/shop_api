from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from ..models import Order
from ..serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class OrderListCreateView(ListCreateAPIView):
    """
    GET: List orders (user sees their orders, admin sees all)
    POST: Create order (authenticated users)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter orders based on user role."""
        user = self.request.user
        
        if user.is_staff or user.is_admin:
            # Admin sees all orders
            return Order.objects.select_related('user').prefetch_related('items').all()
        
        # Regular users see only their orders
        return Order.objects.filter(user=user).prefetch_related('items')
    
    def get_serializer_class(self):
        """Use different serializers for list vs create."""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer


class OrderRetrieveView(RetrieveAPIView):
    """
    GET: Retrieve order detail (owner or admin only)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """Filter orders based on user role."""
        user = self.request.user
        
        if user.is_staff or user.is_admin:
            # Admin sees all orders
            return Order.objects.select_related('user').prefetch_related('items__product').all()
        
        # Regular users see only their orders
        return Order.objects.filter(user=user).prefetch_related('items__product')

