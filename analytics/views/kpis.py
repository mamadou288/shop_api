"""
KPIs API Views with caching.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from ..services import get_business_kpis, get_product_kpis, get_user_kpis


class DashboardKPIsView(APIView):
    """
    GET: All KPIs combined (business, products, users)
    Admin only, cached for 15 minutes.
    
    Query params:
        - start_date: YYYY-MM-DD (default: 90 days ago)
        - end_date: YYYY-MM-DD (default: today)
        - period: 7d|30d|90d|1y (shortcut for date range)
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Parse query params
        start_date, end_date = self._parse_dates(request)
        
        # Create cache key
        cache_key = f"analytics:dashboard:{start_date.date()}:{end_date.date()}"
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Calculate KPIs
        business_kpis = get_business_kpis(start_date, end_date)
        product_kpis = get_product_kpis()
        user_kpis = get_user_kpis(start_date, end_date)
        
        data = {
            'business': business_kpis,
            'products': product_kpis,
            'users': user_kpis,
            'generated_at': timezone.now().isoformat(),
        }
        
        # Cache for 15 minutes (900 seconds)
        cache.set(cache_key, data, timeout=900)
        
        return Response(data)
    
    def _parse_dates(self, request):
        """Parse start_date and end_date from query params."""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)  # Default: 90 days
        
        # Check for period shortcut
        period = request.query_params.get('period')
        if period:
            period_days = {
                '7d': 7,
                '30d': 30,
                '90d': 90,
                '1y': 365,
            }
            days = period_days.get(period, 90)
            start_date = end_date - timedelta(days=days)
        else:
            # Check for explicit dates
            if request.query_params.get('start_date'):
                try:
                    from datetime import datetime
                    start_date = datetime.fromisoformat(request.query_params['start_date'])
                    start_date = timezone.make_aware(start_date) if timezone.is_naive(start_date) else start_date
                except ValueError:
                    pass
            
            if request.query_params.get('end_date'):
                try:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(request.query_params['end_date'])
                    end_date = timezone.make_aware(end_date) if timezone.is_naive(end_date) else end_date
                except ValueError:
                    pass
        
        return start_date, end_date


class BusinessKPIsView(APIView):
    """
    GET: Business KPIs only (revenue, orders, AOV, growth, CLV, repeat rate)
    Admin only, cached for 15 minutes.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Parse query params
        start_date, end_date = self._parse_dates(request)
        
        # Create cache key
        cache_key = f"analytics:business:{start_date.date()}:{end_date.date()}"
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Calculate KPIs
        data = get_business_kpis(start_date, end_date)
        data['generated_at'] = timezone.now().isoformat()
        
        # Cache for 15 minutes
        cache.set(cache_key, data, timeout=900)
        
        return Response(data)
    
    def _parse_dates(self, request):
        """Parse start_date and end_date from query params."""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)
        
        period = request.query_params.get('period')
        if period:
            period_days = {'7d': 7, '30d': 30, '90d': 90, '1y': 365}
            days = period_days.get(period, 90)
            start_date = end_date - timedelta(days=days)
        else:
            if request.query_params.get('start_date'):
                try:
                    from datetime import datetime
                    start_date = datetime.fromisoformat(request.query_params['start_date'])
                    start_date = timezone.make_aware(start_date) if timezone.is_naive(start_date) else start_date
                except ValueError:
                    pass
            
            if request.query_params.get('end_date'):
                try:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(request.query_params['end_date'])
                    end_date = timezone.make_aware(end_date) if timezone.is_naive(end_date) else end_date
                except ValueError:
                    pass
        
        return start_date, end_date


class ProductKPIsView(APIView):
    """
    GET: Product KPIs only (top products, stock alerts, categories)
    Admin only, cached for 15 minutes.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Create cache key
        cache_key = "analytics:products:all"
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Calculate KPIs
        data = get_product_kpis()
        data['generated_at'] = timezone.now().isoformat()
        
        # Cache for 15 minutes
        cache.set(cache_key, data, timeout=900)
        
        return Response(data)


class UserKPIsView(APIView):
    """
    GET: User KPIs only (total, new, active, top customers, retention)
    Admin only, cached for 15 minutes.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Parse query params
        start_date, end_date = self._parse_dates(request)
        
        # Create cache key
        cache_key = f"analytics:users:{start_date.date()}:{end_date.date()}"
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Calculate KPIs
        data = get_user_kpis(start_date, end_date)
        data['generated_at'] = timezone.now().isoformat()
        
        # Cache for 15 minutes
        cache.set(cache_key, data, timeout=900)
        
        return Response(data)
    
    def _parse_dates(self, request):
        """Parse start_date and end_date from query params."""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)
        
        period = request.query_params.get('period')
        if period:
            period_days = {'7d': 7, '30d': 30, '90d': 90, '1y': 365}
            days = period_days.get(period, 90)
            start_date = end_date - timedelta(days=days)
        else:
            if request.query_params.get('start_date'):
                try:
                    from datetime import datetime
                    start_date = datetime.fromisoformat(request.query_params['start_date'])
                    start_date = timezone.make_aware(start_date) if timezone.is_naive(start_date) else start_date
                except ValueError:
                    pass
            
            if request.query_params.get('end_date'):
                try:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(request.query_params['end_date'])
                    end_date = timezone.make_aware(end_date) if timezone.is_naive(end_date) else end_date
                except ValueError:
                    pass
        
        return start_date, end_date

