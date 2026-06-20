from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from uuid import uuid4
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse
from .serializers import UserSerializer
#from .authentication import MongoJWTAuthentication

# Create your views here.

def name(request):
    return HttpResponse("My name is Precious")



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
                email=validated_data["email"])
                user.set_password(validated_data["password"])
                user.save()
                return Response({"success":"user registered successfully"}, status=201)
            else:
                return Response({"error":"forbidden"}, status=403)
        except Exception as e:
            return Response({"error":str(e)},status=400)

