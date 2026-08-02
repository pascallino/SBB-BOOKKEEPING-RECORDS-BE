# subscriptions/permissions.py

from datetime import datetime
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import Subscription
from .models import Customer
from .models import Invoice


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




class CanCreateCustomer(BasePermission):

    message = "You have reached the maximum number of customers allowed by your subscription."

    def has_permission(self, request, view):

        subscription = Subscription.objects.get(
            userid=request.user,
            status="active"
        )

        plan = subscription.planid

        # Unlimited customers
        if plan.max_customers == -1:
            return True

        customer_count = Customer.objects.filter(
            userid=request.user
        ).count()

        if customer_count >= plan.max_customers:
            raise PermissionDenied(self.message)

        return True

class CanCreateInvoice(BasePermission):

    message = "You have reached the maximum number of invoices allowed by your subscription."

    def has_permission(self, request, view):

        subscription = Subscription.objects.get(
            userid=request.user,
            status="active"
        )

        plan = subscription.planid

        # Unlimited invoices
        if plan.max_invoices == -1:
            return True

        invoice_count = Invoice.objects.filter(
            userid=request.user
        ).count()

        if invoice_count >= plan.max_invoices:
            raise PermissionDenied(self.message)

        return True