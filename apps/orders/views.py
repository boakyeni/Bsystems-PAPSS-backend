from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .models import Order, OrderDetail, Invoice
from rest_framework import generics, filters, status
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderDetailSerializer, InvoiceSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
import collections
from apps.inventory.models import Product
from datetime import timedelta
from django.utils.timezone import localtime, now
from rest_framework_simplejwt.authentication import JWTAuthentication


class SearchOrder(generics.ListAPIView):
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["placed_by"]

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset


class SearchUsersOrder(generics.ListAPIView):
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["placed_to"]

    def get_queryset(self):
        queryset = Order.objects.filter(placed_by=self.request.user.id)
        return queryset


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def create_order(request):
    data = request.data
    data["placed_by"] = request.user.id
    company = Product.objects.get(id=data["products"][0]["id"]).seller
    data["placed_to"] = company.id
    order_serializer = OrderSerializer(data=data)
    order_serializer.is_valid(raise_exception=True)
    order_instance = order_serializer.save()

    for product in data["products"]:
        product_instance = Product.objects.get(id=product["id"])
        subtotal = product_instance.cost * product["quantity"]
        order_detail_data = {
            "order": order_instance.id,
            "item_code": product_instance.id,
            "quantity": product["quantity"],
            "subtotal": subtotal,
        }
        order_detail_serializer = OrderDetailSerializer(data=order_detail_data)
        order_detail_serializer.is_valid(raise_exception=True)
        order_detail_serializer.save()

    # Create and Send Proforma Invoice to buyer
    data["buyer"] = request.user.id
    data["issuer"] = company.id
    data["order"] = order_instance.id
    if "shipping_street" in data:
        data["require_shipment"] = True
    invoice_serializer = InvoiceSerializer(data=data)
    invoice_serializer.is_valid(raise_exception=True)
    invoice_instance = invoice_serializer.save()
    order_instance.send_order_request_by_email()
    invoice_instance.send_invoice_by_email()

    return Response(order_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
@transaction.atomic
def edit_order(request):
    data = request.data
    order_instance = Order.objects.get(id=data["order"])
    if order_instance.order_date + timedelta(hours=48) < now():
        return Response(
            {
                # customize your response format here
                "errors": "Cannot cancel order after 48 hours",
                "status": 400,
                "message": "Please contact seller to cancel",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    order_serializer = OrderSerializer(instance=order_instance, partial=True, data=data)
    order_serializer.is_valid(raise_exception=True)
    order_serializer.save()
    return Response(order_serializer.data, status=status.HTTP_200_OK)
