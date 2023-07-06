from django.urls import path,include
from .views import * 
urlpatterns = [
    path('update_wilayas', update_wilayas,name="update_wilayas"),
    path('update_communes', update_communes,name="update_communes"),       
]