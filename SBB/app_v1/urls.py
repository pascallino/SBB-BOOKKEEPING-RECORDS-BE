from django.contrib import admin
from django.urls import path, include
from .views import (name, register, login 
      ,profile, get_all_profile, Post_Income, CreateCustomer, 
      DeleteCustomer, UpdateCustomer, GetCustomer, ListALlCustomers, 
      CreateInvoice, UpdateInvoice, DeleteInvoice, SearchInvoice)


urlpatterns = [
      path('whatismyname', name, name="this api is used to find a customer") ,
      path('api/auth/register', register.as_view(), name="this api is used to register a user") ,
      path('api/auth/login', login.as_view(), name="this api is used to signin a user") ,
      path('api/auth/profile/<email>', profile.as_view(), name="this api is used to update a user") ,
      path('api/auth/profile', get_all_profile.as_view(), name="this api is used to find all users") ,
      path('api/invoice/create', CreateInvoice.as_view(), name="this api is used to create an invoice") ,
      path('api/invoice/update/<id>', UpdateInvoice.as_view(), name="this api is used to modify an invoice") ,
      path("api/invoice/delete/<str:invoice_no>", DeleteInvoice.as_view(), name="delete-invoice"),
      path("api/invoices/search", SearchInvoice.as_view(), name="search-invoice"),
      path('api/customers/create', CreateCustomer.as_view(), name="this api is used to create a customer") ,
      path('api/customers/update/<customerid>', UpdateCustomer.as_view(), name="this api is used to Update a customer") ,
      path('api/customers/delete/<customerid>', DeleteCustomer.as_view(), name="this api is used to Delete a customer") ,
      path('api/customers/get/<customerid>', GetCustomer.as_view(), name="this api is used to find a customer") ,
       path('api/customers', ListALlCustomers.as_view(), name="this api is used to find all customer") ,

      
      path('api/income', Post_Income.as_view(), name="this api is used to add an Income") ,
]
