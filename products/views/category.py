from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from products.models import Category
from products.serializers import CategorySerializer


class CategoryListCreateView(ListCreateAPIView):
    """
    GET: List all active categories
    POST: Create a new category (admin only)
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        """
        Allow anyone to view (GET), admin only for create (POST).
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a category by slug
    PATCH: Update a category (admin only)
    DELETE: Delete a category (admin only)
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """
        Allow anyone to view (GET), admin only for modifications.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

