from .models import  User, Income, Customer, Invoice
from rest_framework_mongoengine import serializers

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model=User
        fields='__all__'

class InvoiceSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Invoice
        fields='__all__'

class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Customer
        fields='__all__'

class IncomeSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Income
        fields='__all__'
        
