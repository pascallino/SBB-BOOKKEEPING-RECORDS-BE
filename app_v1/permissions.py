# subscriptions/permissions.py

from datetime import datetime
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import Subscription


class HasActiveSubscription(BasePermission):
    message = "Your subscription has expired. Please renew your subscription."

    def has_permission(self, request, view):

        try:
            subscription = Subscription.objects.get(userid=request.user)

            # Automatically expire the subscription if needed
            if (
                subscription.status == "active"
                and datetime.utcnow() > subscription.end_date
            ):
                subscription.status = "expired"
                subscription.updated_at = datetime.utcnow()
                subscription.save()

            if subscription.status != "active":
                return False

            return True

        except Subscription.DoesNotExist:
            raise PermissionDenied(
                "No active subscription found. Please subscribe to continue."
            )