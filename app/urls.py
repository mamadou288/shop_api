from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/auth/', include('accounts.urls')),
    
    # API Products (categories + products)
    path('api/', include('products.urls')),
]
