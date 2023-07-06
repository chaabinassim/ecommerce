from django.urls import path
from .views import *

urlpatterns = [
    path('<int:order_id>',order_success, name='order_success'),
    path('cart',cart, name='cart'),
    
]
