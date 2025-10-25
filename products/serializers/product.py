from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from products.models import Product, ProductImage
from .category import CategoryListSerializer


class ProductImageSerializer(ModelSerializer):
    """
    Product image serializer.
    """
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']
        read_only_fields = ['id']


class ProductSerializer(ModelSerializer):
    """
    Detailed product serializer with nested category and images.
    """
    
    category_detail = CategoryListSerializer(source='category', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_in_stock = SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'category',
            'category_detail',
            'sku',
            'images',
            'is_in_stock',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'is_in_stock']
    
    def get_is_in_stock(self, obj):
        return obj.is_in_stock
    
    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise ValidationError("Price must be positive")
        return value
    
    def validate_stock(self, value):
        """Validate stock is not negative"""
        if value < 0:
            raise ValidationError("Stock cannot be negative")
        return value


class ProductListSerializer(ModelSerializer):
    """
    Lightweight product serializer for list views.
    """
    
    category_name = SerializerMethodField()
    thumbnail = SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'stock',
            'category_name',
            'thumbnail',
            'is_active',
        ]
    
    def get_category_name(self, obj):
        return obj.category.name
    
    def get_thumbnail(self, obj):
        """Get first image"""
        first_image = obj.images.filter(is_active=True).first()
        if first_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
        return None


class ProductCreateUpdateSerializer(ModelSerializer):
    """
    Serializer for creating/updating products.
    """
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'stock',
            'category',
            'sku',
            'is_active',
        ]

