from django.db import models
from django.db import models
from mongoengine import Document, ListField, StringField, EmailField, DateField, DateTimeField, FloatField
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from uuid import uuid4
# Create your models here.


class User(Document):
    first_name = StringField()
    last_name = StringField()
    email = EmailField(unique=True)
    password = StringField()
    business_name = StringField()
    created_at = DateTimeField()
