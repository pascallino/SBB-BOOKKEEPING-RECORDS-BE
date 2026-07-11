from .models import  User, Income, Customer, Invoice, Expense, Vendor
from rest_framework_mongoengine import serializers


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model=User
        fields='__all__'

class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Customer
        fields='__all__'

class SInvoiceSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Invoice
        fields='__all__'


class IncomeSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Income
        fields='__all__'

class SIncomeSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Income
        fields='__all__'

class ExpenseSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Expense
        fields='__all__'

class SExpenseSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Expense
        fields='__all__'

class VendorSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Vendor
        fields='__all__'


from rest_framework import serializers
class CreateInvoiceSerializer(serializers.Serializer):
    customerid = serializers.CharField(required=False)
    amount = serializers.FloatField()
    due_date = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(
        choices=["paid", "unpaid", "partial"]
    )
        
class CreateIncomeSerializer(serializers.Serializer):
    incomeid = serializers.CharField(read_only=True)
    invoice_no = serializers.CharField(required=False, allow_null=True)
    source = serializers.CharField(max_length=255)
    amount = serializers.FloatField()
    description = serializers.CharField(required=False, allow_blank=True)
    transaction_date = serializers.DateTimeField()

