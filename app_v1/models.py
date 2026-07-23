from django.db import models
from django.db import models
from mongoengine import (Document, ReferenceField,
      ListField, StringField, EmailField, DateField,
      DateTimeField, FloatField, IntField, BooleanField)
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from uuid import uuid4
# Create your models here.

class User(Document):
    userid = StringField()
    first_name = StringField()
    last_name = StringField()
    email = EmailField(unique=True)
    password = StringField()
    business_name = StringField()
    created_at = DateTimeField()
    
    def set_password(self, password):
      self.password = make_password(password)

    def check_password(self, password):
      return check_password(password, self.password)

    @property
    def is_authenticated(self):
        return True


class Customer(Document):
    userid = ReferenceField(User)
    customerid = StringField()
    first_name = StringField()
    last_name = StringField()
    business_name = StringField()
    email = EmailField()
    phone_number = StringField()
    address = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

class Invoice(Document):
    userid = ReferenceField(User)
    customer_id = ReferenceField(Customer, null=True)
    invoice_no = StringField()
    amount = FloatField()
    due_date = DateTimeField(required=False)
    status = StringField(
        choices=["paid", "unpaid", "partial"]
    )
    created_at = DateTimeField()
    updated_at = DateTimeField()

""" class Invoice(Document):
    userid = ReferenceField(User,  null=True)
    invoice_number = StringField()
    customerid = ReferenceField(Customer)
    amount = FloatField()
    status = StringField(
        choices=["paid", "unpaid", "partial"]
    )

    due_date = DateTimeField()
    created_at = DateTimeField() """


class Income(Document):
    incomeid = StringField()
    userid = ReferenceField(User)
    invoiceid = ReferenceField(Invoice, null=True)
    source = StringField()
    amount = FloatField()
    description = StringField()
    transaction_date = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class Expense(Document):
    expenseid = StringField()
    userid = ReferenceField(User)
    category = StringField()
    amount = FloatField()
    description = StringField()
    expense_date = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class Vendor(Document):
    vendorid = StringField()
    userid = ReferenceField(User)
    business_name = StringField()
    contact_person = StringField()
    email = EmailField()
    phone = StringField()
    address = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    

class Plan(Document):
    planid = StringField()
    name = StringField()          # Basic, Pro, Enterprise
    price = FloatField()
    billing_cycle = StringField(
        choices=["monthly", "yearly"]
    )
    max_customers = IntField()
    max_invoices = IntField()
    max_users = IntField()
    active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)