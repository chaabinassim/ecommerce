from django.urls import path
from .views import *

urlpatterns = [
    path('order-success/<int:order_id>',order_success, name='order_success'),
    path('download_bill/<int:order_id>/', generate_pdf_bill, name='download_bill'),
    path('',cart, name='cart'),
    
]
