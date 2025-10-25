"""
Business KPIs service - Revenue, orders, growth metrics.
"""
from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q, Case, When, IntegerField
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderStatus


def get_business_kpis(start_date=None, end_date=None):
    """
    Calculate business KPIs for the given period.
    
    Args:
        start_date: Start date for filtering (default: 3 months ago)
        end_date: End date for filtering (default: now)
    
    Returns:
        dict: Business KPIs including revenue, orders, AOV, growth, CLV, repeat rate
    """
    now = timezone.now()
    
    # Default dates: last 3 months
    if not end_date:
        end_date = now
    if not start_date:
        start_date = end_date - timedelta(days=90)
    
    # Filter orders in period
    orders_in_period = Order.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,
    )
    
    # === ESSENTIAL KPIs ===
    
    # Total revenue (only DELIVERED orders)
    total_revenue = orders_in_period.filter(
        status=OrderStatus.DELIVERED
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')
    
    # Total orders by status
    orders_by_status = orders_in_period.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    status_breakdown = {item['status']: item['count'] for item in orders_by_status}
    total_orders = orders_in_period.count()
    
    # Average Order Value (AOV) - only DELIVERED
    delivered_orders = orders_in_period.filter(status=OrderStatus.DELIVERED)
    aov = delivered_orders.aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0.00')
    
    # Revenue by month (for line chart)
    revenue_by_month = []
    current = start_date.replace(day=1)
    while current <= end_date:
        next_month = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        month_revenue = Order.objects.filter(
            created_at__gte=current,
            created_at__lt=next_month,
            status=OrderStatus.DELIVERED
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        revenue_by_month.append({
            'month': current.strftime('%Y-%m'),
            'revenue': float(month_revenue),
        })
        
        current = next_month
    
    # Orders by status (for pie chart)
    orders_status_chart = [
        {
            'status': status,
            'label': dict(OrderStatus.choices).get(status, status),
            'count': status_breakdown.get(status, 0)
        }
        for status in OrderStatus.values
    ]
    
    # === ADVANCED KPIs ===
    
    # MoM Growth Rate (Month-over-Month)
    mom_growth = _calculate_mom_growth(end_date)
    
    # Customer Lifetime Value (CLV)
    clv = _calculate_clv()
    
    # Repeat Purchase Rate
    repeat_rate = _calculate_repeat_purchase_rate()
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        },
        'revenue': {
            'total': float(total_revenue),
            'currency': 'EUR',
            'growth': mom_growth['revenue_growth'],
        },
        'orders': {
            'total': total_orders,
            'by_status': status_breakdown,
            'status_chart': orders_status_chart,
            'growth': mom_growth['orders_growth'],
        },
        'aov': {
            'value': float(aov),
            'currency': 'EUR',
        },
        'clv': {
            'value': float(clv),
            'currency': 'EUR',
        },
        'repeat_purchase_rate': {
            'percentage': repeat_rate,
        },
        'charts': {
            'revenue_by_month': revenue_by_month,
        }
    }


def _calculate_mom_growth(end_date):
    """
    Calculate Month-over-Month growth for revenue and orders.
    
    Returns:
        dict: Revenue and orders growth percentages
    """
    # Current month (last 30 days from end_date)
    current_month_start = end_date - timedelta(days=30)
    current_month_end = end_date
    
    # Previous month (30 days before current month)
    previous_month_start = current_month_start - timedelta(days=30)
    previous_month_end = current_month_start
    
    # Current month metrics
    current_revenue = Order.objects.filter(
        created_at__gte=current_month_start,
        created_at__lte=current_month_end,
        status=OrderStatus.DELIVERED
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    current_orders = Order.objects.filter(
        created_at__gte=current_month_start,
        created_at__lte=current_month_end
    ).count()
    
    # Previous month metrics
    previous_revenue = Order.objects.filter(
        created_at__gte=previous_month_start,
        created_at__lte=previous_month_end,
        status=OrderStatus.DELIVERED
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    previous_orders = Order.objects.filter(
        created_at__gte=previous_month_start,
        created_at__lte=previous_month_end
    ).count()
    
    # Calculate growth percentages
    revenue_growth = 0.0
    if previous_revenue > 0:
        revenue_growth = float(((current_revenue - previous_revenue) / previous_revenue) * 100)
    
    orders_growth = 0.0
    if previous_orders > 0:
        orders_growth = ((current_orders - previous_orders) / previous_orders) * 100
    
    return {
        'revenue_growth': round(revenue_growth, 2),
        'orders_growth': round(orders_growth, 2),
    }


def _calculate_clv():
    """
    Calculate Customer Lifetime Value (CLV).
    Average revenue per paying customer.
    
    Returns:
        Decimal: CLV value
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Total revenue from all delivered orders
    total_revenue = Order.objects.filter(
        status=OrderStatus.DELIVERED
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    # Number of customers with at least one order
    customers_with_orders = User.objects.filter(
        orders__status=OrderStatus.DELIVERED
    ).distinct().count()
    
    if customers_with_orders == 0:
        return Decimal('0.00')
    
    clv = total_revenue / customers_with_orders
    return round(clv, 2)


def _calculate_repeat_purchase_rate():
    """
    Calculate Repeat Purchase Rate.
    Percentage of customers with 2+ orders.
    
    Returns:
        float: Repeat purchase rate percentage
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Total customers with at least one order
    total_customers = User.objects.filter(orders__isnull=False).distinct().count()
    
    if total_customers == 0:
        return 0.0
    
    # Customers with 2+ orders
    repeat_customers = User.objects.annotate(
        order_count=Count('orders')
    ).filter(order_count__gte=2).count()
    
    repeat_rate = (repeat_customers / total_customers) * 100
    return round(repeat_rate, 2)

