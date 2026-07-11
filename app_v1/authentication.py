from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        userid = validated_token.get("userid")

        if not userid:
            raise AuthenticationFailed("User ID missing")

        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")