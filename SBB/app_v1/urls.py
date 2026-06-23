from django.contrib import admin
from django.urls import path, include
from .views import (name, register, login 
      ,profile, get_all_profile, Post_Income)


urlpatterns = [
      path('whatismyname', name, name="this api is used to find a customer") ,
      path('api/auth/register', register.as_view(), name="this api is used to register a user") ,
      path('api/auth/login', login.as_view(), name="this api is used to signin a user") ,
      path('api/auth/profile/<email>', profile.as_view(), name="this api is used to update a user") ,
      path('api/auth/profile', get_all_profile.as_view(), name="this api is used to find all users") ,
       path('api/income', Post_Income.as_view(), name="this api is used to add an Income") ,
]
