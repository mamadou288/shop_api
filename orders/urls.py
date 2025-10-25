from django.urls import path
from .views import (
    OrderListCreateView,
    OrderRetrieveView,
    OrderCancelView,
    OrderConfirmView,
    OrderShipView,
    OrderDeliverView,
)

urlpatterns = [
    # Orders
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<uuid:pk>/', OrderRetrieveView.as_view(), name='order-detail'),
    
    # Actions
    path('<uuid:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('<uuid:pk>/confirm/', OrderConfirmView.as_view(), name='order-confirm'),
    path('<uuid:pk>/ship/', OrderShipView.as_view(), name='order-ship'),
    path('<uuid:pk>/deliver/', OrderDeliverView.as_view(), name='order-deliver'),
]

