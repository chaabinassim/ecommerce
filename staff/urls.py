from django.urls import path
from .views import *

urlpatterns = [
    path('orders',staff_view, name='staff_view'),
    path('orders/<pk>/update', OrderUpdateView.as_view(),name="staff_order_update"), 
]
