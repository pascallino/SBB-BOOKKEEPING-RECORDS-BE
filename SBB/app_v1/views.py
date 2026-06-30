from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Income, Invoice, Customer
from uuid import uuid4
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse
from .serializers import (UserSerializer, IncomeSerializer, 
                          CustomerSerializer, CreateInvoiceSerializer,
                          SInvoiceSerializer)
from datetime  import datetime
from .authentication import MongoJWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def name(request):
    return HttpResponse("My name is Precious")

""" POST   SBB/v1/api/auth/register/
POST   SBB/v1/api/auth/login
GET    SBB/v1/api/auth/profile/
PUT    SBB/v1/api/auth/profile/ """

class register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = UserSerializer(data=request.data)
            if data.is_valid():
                validated_data = data.validated_data
                user = User(userid=str(uuid4()),
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email=validated_data["email"],
                business_name = validated_data["business_name"],
                created_at = datetime.now())
                user.set_password(validated_data["password"])
                user.save()
                return Response({"success":"user registered successfully"}, status=201)
            else:
                return Response({"error":"forbidden"}, status=403)
        except Exception as e:
            return Response({"error":str(e)},status=400)



class login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not user.check_password(password):
            return Response(
                {"detail": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        token = AccessToken()
        token["userid"] = str(user.userid)
        token["email"] = user.email
        response = Response(
            {
                "message": "Login successful",
                "access": str(token)
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=str(token),
            httponly=False,   # True in production
            secure=False,     # True in production (HTTPS)
            samesite="Lax",
            max_age=420
        )

        return response

class profile(APIView):
    authentication_classes = [MongoJWTAuthentication]
    #permission_classes = [AllowAny]
    def put(self, request, email):
        try:
            user = User.objects.get(email=email)

            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                if "first_name" in validated_data:
                    user.first_name = validated_data.get("first_name", user.first_name)
                if "last_name" in validated_data:
                    user.last_name = validated_data.get("last_name", user.last_name)
                if "email" in validated_data:
                    user.email = validated_data.get("email", user.email)
                if "password" in validated_data:
                    user.set_password(validated_data["password"])
                if "business_name" in validated_data:
                    user.business_name = validated_data.get("business_name", user.business_name)
                user.save()
                return Response(UserSerializer(user).data, status=200)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class get_all_profile(APIView):
    authentication_classes = [MongoJWTAuthentication]
    def get(self, request,):
        try:
            users = User.objects.all()
            serialized_user = UserSerializer(users, many=True)
            return Response(serialized_user.data, status=200)
        except User.DoesNotExist:
            return Response({"error":"User not found"}, status=400)

class CreateInvoice(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = CreateInvoiceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            customer = None
            customerid = validated_data.get("customerid")
            if customerid:
                customer = Customer.objects.get(customerid=customerid)
            invoice = Invoice(
                userid=request.user,
                customer_id=customer,
                invoice_no=f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}",
                amount=validated_data["amount"],
                due_date=validated_data.get("due_date"),
                status=validated_data["status"],
                created_at=datetime.now()
            )
            invoice.save()
            return Response(
                {"success": "Invoice registered successfully"},
                status=201
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=404
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )


class UpdateInvoice(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            serializer = CreateInvoiceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            # Get invoice belonging to the authenticated user
            invoice = Invoice.objects.get(id=id, userid=request.user)

            # Update customer if provided
            customerid = validated_data.get("customerid")
            if customerid:
                customer = Customer.objects.get(customerid=customerid)
                invoice.customer_id = customer

            # Update invoice fields
            invoice.amount = validated_data["amount"]
            invoice.due_date = validated_data.get("due_date")
            invoice.status = validated_data["status"]
            invoice.updated_at = datetime.now()

            invoice.save()

            return Response(
                {"success": "Invoice updated successfully"},
                status=200
            )

        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=404
            )

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=404
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

class SearchInvoice(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            invoice_no = request.GET.get("invoice_no")
            start_date = request.GET.get("start_date")
            end_date = request.GET.get("end_date")
            invoices = Invoice.objects.filter(userid=request.user)
            # Filter by invoice number
            if invoice_no:
                invoices = invoices.filter(invoice_no__icontains=invoice_no)
            # Filter by start date
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                invoices = invoices.filter(created_at__gte=start_date)

            # Filter by end date
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").replace(
                    hour=23, minute=59, second=59
                )
                invoices = invoices.filter(created_at__lte=end_date)

            serializer = SInvoiceSerializer(invoices, many=True)

            return Response(serializer.data, status=200)

        except ValueError:
            return Response(
                {"error": "Date format should be YYYY-MM-DD"},
                status=400
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

class DeleteInvoice(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, invoice_no):
        try:
            invoice = Invoice.objects.get(
                invoice_no=invoice_no,
                userid=request.user
            )
            invoice.delete()
            return Response(
                {"success": "Invoice deleted successfully"},
                status=200
            )
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=404
            )


class CreateCustomer(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = CustomerSerializer(data=request.data)
            data.is_valid(raise_exception=True)
            validated_data = data.validated_data
            customer = Customer(customerid=str(uuid4()),
            userid=request.user,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            business_name=validated_data["business_name"],
            email=validated_data["email"],
            phone_number = validated_data["phone_number"],
            address = validated_data["address"],
            created_at = datetime.now(),
            updated_at = datetime.now())
            customer.save()
            return Response({"success":"Customer registered successfully"}, status=201)
        except Exception as e:
            return Response({"error":str(e)},status=400)
        

class UpdateCustomer(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, customerid):
        try:
            customer = Customer.objects.get(customerid=customerid)
            serializer = CustomerSerializer(
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            for key, value in serializer.validated_data.items():
                setattr(customer, key, value)
            customer.updated_at = datetime.now()
            customer.save()
            return Response(
                {"success": "Customer updated successfully"},
                status=200
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=404
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

class DeleteCustomer(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, customerid):
        try:
            customer = Customer.objects.get(customerid=customerid)
            customer.delete()
            return Response(
                {"success": "Customer deleted successfully"},
                status=200
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=404
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )

class GetCustomer(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, customerid):
        try:
            customer = Customer.objects.get(customerid=customerid)
            serialized_customer = CustomerSerializer(customer)
            return Response(serialized_customer.data, status=200)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found"}, status=400)

class ListALlCustomers(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            customers = Customer.objects.all()
            serialized_customer = CustomerSerializer(customers, many=True)
            return Response(serialized_customer.data, status=200)
        except Customer.DoesNotExist:
            return Response({"error":"Customer not found"}, status=400)


class Post_Income(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = IncomeSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                invoice = None
                invoiceid = validated_data.get("invoiceid")
                if invoiceid:
                    invoice = Invoice.objects.get(id=invoiceid)
                income = Income(
                    incomeid =str(uuid4()),
                    userid=request.user,
                    invoiceid=invoice,
                    source=validated_data["source"],
                    amount=validated_data["amount"],
                    description=validated_data.get("description"),
                    transaction_date=datetime.now(),
                    created_at=datetime.now()
                )
                income.save()
                return Response({
                    "success": "Income created successfully",
                    "income_id": str(income.id)
                }, status=201)
            return Response(serializer.errors, status=400)
        except Invoice.DoesNotExist:
            return Response({
                "error": "Invoice not found"
            }, status=404)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=400)



            