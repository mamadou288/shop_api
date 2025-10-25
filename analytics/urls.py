from django.urls import path
from .views import (
    DashboardKPIsView,
    BusinessKPIsView,
    ProductKPIsView,
    UserKPIsView,
)

urlpatterns = [
    path('dashboard/', DashboardKPIsView.as_view(), name='analytics-dashboard'),
    path('business/', BusinessKPIsView.as_view(), name='analytics-business'),
    path('products/', ProductKPIsView.as_view(), name='analytics-products'),
    path('users/', UserKPIsView.as_view(), name='analytics-users'),
]

