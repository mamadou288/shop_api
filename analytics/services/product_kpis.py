"""
Product KPIs service - Top products, stock alerts, categories.
"""
from django.db.models import Sum, Count, Q, F
from orders.models import OrderItem, OrderStatus
from products.models import Product, Category


def get_product_kpis():
    """
    Calculate product-related KPIs.
    
    Returns:
        dict: Product KPIs including top products, stock alerts, categories
    """
    
    # === TOP PRODUCTS BY REVENUE ===
    top_products_revenue = OrderItem.objects.filter(
        order__status=OrderStatus.DELIVERED
    ).values(
        'product__id',
        'product__name',
        'product__slug',
        'product__price',
    ).annotate(
        total_revenue=Sum(F('product_price') * F('quantity')),
        units_sold=Sum('quantity')
    ).order_by('-total_revenue')[:10]
    
    # === TOP PRODUCTS BY QUANTITY ===
    top_products_quantity = OrderItem.objects.filter(
        order__status=OrderStatus.DELIVERED
    ).values(
        'product__id',
        'product__name',
        'product__slug',
    ).annotate(
        units_sold=Sum('quantity'),
        total_revenue=Sum(F('product_price') * F('quantity'))
    ).order_by('-units_sold')[:10]
    
    # === STOCK ALERTS ===
    
    # Low stock (stock < 10 but > 0)
    low_stock_products = Product.objects.filter(
        stock__gt=0,
        stock__lt=10,
        is_active=True
    ).values(
        'id', 'name', 'slug', 'stock', 'price'
    ).order_by('stock')[:20]
    
    # Out of stock
    out_of_stock_products = Product.objects.filter(
        stock=0,
        is_active=True
    ).values(
        'id', 'name', 'slug', 'price'
    ).count()
    
    # === CATEGORIES PERFORMANCE ===
    
    # Top categories by revenue
    top_categories = OrderItem.objects.filter(
        order__status=OrderStatus.DELIVERED
    ).values(
        'product__category__id',
        'product__category__name',
        'product__category__slug',
    ).annotate(
        total_revenue=Sum(F('product_price') * F('quantity')),
        units_sold=Sum('quantity'),
        products_count=Count('product__id', distinct=True)
    ).order_by('-total_revenue')[:10]
    
    # Products count by category
    category_distribution = Category.objects.annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).values('id', 'name', 'product_count').order_by('-product_count')[:10]
    
    # === INVENTORY VALUE ===
    
    # Total stock value (price × stock)
    inventory_value = Product.objects.filter(
        is_active=True
    ).annotate(
        stock_value=F('price') * F('stock')
    ).aggregate(
        total=Sum('stock_value')
    )['total'] or 0
    
    return {
        'top_products': {
            'by_revenue': [
                {
                    'id': str(item['product__id']),
                    'name': item['product__name'],
                    'slug': item['product__slug'],
                    'price': float(item['product__price']),
                    'revenue': float(item['total_revenue']),
                    'units_sold': item['units_sold'],
                }
                for item in top_products_revenue
            ],
            'by_quantity': [
                {
                    'id': str(item['product__id']),
                    'name': item['product__name'],
                    'slug': item['product__slug'],
                    'units_sold': item['units_sold'],
                    'revenue': float(item['total_revenue']),
                }
                for item in top_products_quantity
            ],
        },
        'stock_alerts': {
            'low_stock': [
                {
                    'id': str(item['id']),
                    'name': item['name'],
                    'slug': item['slug'],
                    'stock': item['stock'],
                    'price': float(item['price']),
                }
                for item in low_stock_products
            ],
            'out_of_stock_count': out_of_stock_products,
        },
        'categories': {
            'top_by_revenue': [
                {
                    'id': str(item['product__category__id']),
                    'name': item['product__category__name'],
                    'slug': item['product__category__slug'],
                    'revenue': float(item['total_revenue']),
                    'units_sold': item['units_sold'],
                    'products_count': item['products_count'],
                }
                for item in top_categories if item['product__category__id']
            ],
            'distribution': [
                {
                    'id': str(item['id']),
                    'name': item['name'],
                    'product_count': item['product_count'],
                }
                for item in category_distribution
            ],
        },
        'inventory': {
            'total_value': float(inventory_value),
            'currency': 'EUR',
        }
    }

