"""
User KPIs service - User growth, active users, top customers.
"""
from django.db.models import Sum, Count, Q, F
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderStatus

User = get_user_model()


def get_user_kpis(start_date=None, end_date=None):
    """
    Calculate user-related KPIs.
    
    Args:
        start_date: Start date for filtering (default: 3 months ago)
        end_date: End date for filtering (default: now)
    
    Returns:
        dict: User KPIs including total, new, active users, top customers
    """
    now = timezone.now()
    
    # Default dates: last 3 months
    if not end_date:
        end_date = now
    if not start_date:
        start_date = end_date - timedelta(days=90)
    
    # === TOTAL USERS ===
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    
    # === NEW USERS IN PERIOD ===
    new_users = User.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,
        is_staff=False,
        is_superuser=False
    ).count()
    
    # === ACTIVE USERS (with orders in period) ===
    active_users = User.objects.filter(
        orders__created_at__gte=start_date,
        orders__created_at__lte=end_date,
        is_staff=False,
        is_superuser=False
    ).distinct().count()
    
    # === USERS BY REGISTRATION MONTH ===
    users_by_month = []
    current = start_date.replace(day=1)
    while current <= end_date:
        next_month = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        month_users = User.objects.filter(
            created_at__gte=current,
            created_at__lt=next_month,
            is_staff=False,
            is_superuser=False
        ).count()
        
        users_by_month.append({
            'month': current.strftime('%Y-%m'),
            'count': month_users,
        })
        
        current = next_month
    
    # === TOP CUSTOMERS (by total spent) ===
    top_customers = User.objects.filter(
        orders__status=OrderStatus.DELIVERED,
        is_staff=False,
        is_superuser=False
    ).annotate(
        total_spent=Sum('orders__total_amount'),
        order_count=Count('orders', filter=Q(orders__status=OrderStatus.DELIVERED))
    ).order_by('-total_spent')[:10]
    
    top_customers_data = [
        {
            'id': str(user.id),
            'email': user.email,
            'name': user.get_full_name(),
            'total_spent': float(user.total_spent),
            'order_count': user.order_count,
        }
        for user in top_customers
    ]
    
    # === RETENTION RATE ===
    # Users who made orders in both first and second half of period
    mid_period = start_date + (end_date - start_date) / 2
    
    first_half_users = set(
        User.objects.filter(
            orders__created_at__gte=start_date,
            orders__created_at__lt=mid_period
        ).values_list('id', flat=True).distinct()
    )
    
    second_half_users = set(
        User.objects.filter(
            orders__created_at__gte=mid_period,
            orders__created_at__lte=end_date
        ).values_list('id', flat=True).distinct()
    )
    
    retained_users = len(first_half_users & second_half_users)
    retention_rate = 0.0
    if len(first_half_users) > 0:
        retention_rate = (retained_users / len(first_half_users)) * 100
    
    # === USER SEGMENTATION ===
    # Simple segmentation: by order count
    user_segments = {
        'new': User.objects.filter(
            orders__isnull=True,
            is_staff=False,
            is_superuser=False
        ).count(),
        'one_time': User.objects.annotate(
            order_count=Count('orders')
        ).filter(
            order_count=1,
            is_staff=False,
            is_superuser=False
        ).count(),
        'repeat': User.objects.annotate(
            order_count=Count('orders')
        ).filter(
            order_count__gte=2,
            order_count__lt=5,
            is_staff=False,
            is_superuser=False
        ).count(),
        'loyal': User.objects.annotate(
            order_count=Count('orders')
        ).filter(
            order_count__gte=5,
            is_staff=False,
            is_superuser=False
        ).count(),
    }
    
    return {
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        },
        'total_users': total_users,
        'new_users': new_users,
        'active_users': active_users,
        'retention_rate': {
            'percentage': round(retention_rate, 2),
        },
        'top_customers': top_customers_data,
        'users_by_month': users_by_month,
        'segments': user_segments,
    }

