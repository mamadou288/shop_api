from django.db import models
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from products.models import Product
from products.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
)


class ProductListCreateView(ListCreateAPIView):
    """
    GET: List products with filters
    POST: Create a new product (admin only)
    """
    
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def get_permissions(self):
        """Allow anyone to view (GET), admin only for create (POST)."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """Apply custom filters."""
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by stock availability
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(sku__icontains=search)
            )
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a product by slug
    PATCH: Update a product (admin only)
    DELETE: Delete a product (admin only)
    """
    
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.request.method in ['PATCH', 'PUT']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_permissions(self):
        """Allow anyone to view (GET), admin only for modifications."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

