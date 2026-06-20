from django.db import models
from django.db import models
from mongoengine import Document, ListField, StringField, EmailField, DateField, DateTimeField, FloatField
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
