from django.contrib import admin
from django.urls import path, include
from .views import (name, register, login 
      ,profile, get_all_profile, Post_Income, CreateCustomer, 
      DeleteCustomer, UpdateCustomer, GetCustomer, ListALlCustomers, 
      CreateInvoice, UpdateInvoice, DeleteInvoice, SearchInvoice, 
      CreateIncome, ListAllIncome, UpdateIncome, DeleteIncome, SearchIncome,
      CreateCustomer, CreateExpense, ListAllExpenses, UpdateExpense, 
      SearchExpense, DeleteExpense, CreateVendor, ListAllVendors, UpdateVendor,
      DeleteVendor, SearchVendor)


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
      path('api/income/create', CreateIncome.as_view(), name="this api is used to record a Payment") ,
      path('api/income', ListAllIncome.as_view(), name="this api  List All Income Payment") ,
      path('api/income/update/<incomeid>', UpdateIncome.as_view(), name="this api is used to update an Income Payment") ,
      path('api/income/delete/<incomeid>', DeleteIncome.as_view(), name="this api is used to Delete an Income Payment") ,
      path("api/income/search", SearchIncome.as_view(), name="search-Income"),
      path("api/expenses/create", CreateExpense.as_view(), name="Create Expense"),
      path("api/expenses", ListAllExpenses.as_view(), name="List Expenses"),
      path("api/expenses/update/<str:expenseid>", UpdateExpense.as_view(), name="Update Expense"),
      path("api/expenses/delete/<str:expenseid>", DeleteExpense.as_view(), name="Delete Expense"),
      path("api/expenses/search", SearchExpense.as_view(),name="Search Expense"),
      path('api/customers/create', CreateCustomer.as_view(), name="this api is used to create a customer") ,
      path('api/customers/update/<customerid>', UpdateCustomer.as_view(), name="this api is used to Update a customer") ,
      path('api/customers/delete/<customerid>', DeleteCustomer.as_view(), name="this api is used to Delete a customer") ,
      path('api/customers/get/<customerid>', GetCustomer.as_view(), name="this api is used to find a customer") ,
      path('api/customers', ListALlCustomers.as_view(), name="this api is used to find all customer") ,
      path("api/vendor/create", CreateVendor.as_view(), name="Create Vendor"),
      path("api/vendor", ListAllVendors.as_view(),name="List Vendors"),
      path("api/vendor/update/<str:vendorid>", UpdateVendor.as_view(), name="Update Vendor"),
      path("api/vendor/delete/<str:vendorid>", DeleteVendor.as_view(), name="Delete Vendor"),
      path("api/vendor/search", SearchVendor.as_view(),name="Search Vendor"),
     # path('api/income', Post_Income.as_view(), name="this api is used to add an Income") ,
]
