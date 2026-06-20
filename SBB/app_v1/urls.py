from django.contrib import admin
from django.urls import path, include
from .views import name, register


urlpatterns = [
      path('whatismyname', name, name="this api is used to find a customer") ,
      path('api/auth/register', register.as_view(), name="this api is used to register a user") ,
    
]