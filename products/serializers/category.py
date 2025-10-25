from rest_framework.serializers import ModelSerializer, SerializerMethodField
from products.models import Category


class CategorySerializer(ModelSerializer):
    """
    Category serializer with product count.
    """
    
    product_count = SerializerMethodField()
    full_path = SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'image',
            'full_path',
            'product_count',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'full_path', 'product_count']
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    
    def get_full_path(self, obj):
        return obj.get_full_path()


class CategoryListSerializer(ModelSerializer):
    """
    Category serializer for lists.
    """
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

