from django.urls import path
from .views import *

urlpatterns = [
    path('overview',stats_view, name='stats_view'),  
]
