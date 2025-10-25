from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Order
from ..serializers import OrderSerializer


class IsOwnerOrAdmin(IsAuthenticated):
    """
    Permission: Owner or admin only.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or request.user.is_admin


class OrderCancelView(GenericAPIView):
    """
    POST: Cancel order (owner or admin only)
    Restores product stock.
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = OrderSerializer
    
    def post(self, request, pk):
        """Cancel order."""
        # Get order
        order = get_object_or_404(Order, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, order)
        
        # Try to cancel
        try:
            order.cancel()
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Return updated order
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderConfirmView(GenericAPIView):
    """
    POST: Confirm order (admin only)
    """
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    
    def post(self, request, pk):
        """Confirm order."""
        order = get_object_or_404(Order, pk=pk)
        
        try:
            order.confirm()
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderShipView(GenericAPIView):
    """
    POST: Ship order (admin only)
    """
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    
    def post(self, request, pk):
        """Ship order."""
        order = get_object_or_404(Order, pk=pk)
        
        try:
            order.ship()
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class OrderDeliverView(GenericAPIView):
    """
    POST: Deliver order (admin only)
    """
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    
    def post(self, request, pk):
        """Deliver order."""
        order = get_object_or_404(Order, pk=pk)
        
        try:
            order.deliver()
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)

