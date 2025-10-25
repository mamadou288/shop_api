from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    #  Authentication
    path('api/auth/', include('accounts.urls')),
    
    # Products (categories + products)
    path('api/', include('products.urls')),
    
    # Orders
    path('api/orders/', include('orders.urls')),
    
    # Analytics
    path('api/analytics/', include('analytics.urls')),
]
