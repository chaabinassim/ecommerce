from django.urls import path
from .views import *
from django.contrib.auth.decorators import permission_required
urlpatterns = [
    path('',staff_view, name='staff_view'),
    path('update/<pk>/', OrderUpdateView,name="staff_order_update"), 
]
