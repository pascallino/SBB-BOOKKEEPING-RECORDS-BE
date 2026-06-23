from .models import  User, Income
from rest_framework_mongoengine import serializers

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model=User
        fields='__all__'

class IncomeSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Income
        fields='__all__'
        
