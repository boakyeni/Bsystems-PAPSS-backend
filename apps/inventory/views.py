from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.response import Response
from django.db import transaction

# Create your views here.


class SearchProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["name", "description"]

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset


@api_view(["GET"])
def get_number_of_products(request):
    return Response(
        {"uploaded_products": len(Product.objects.all())}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@transaction.atomic
def create_product(request):
    data = request.data

    categories = data["categories"]
    category_instances = []

    for category in categories:
        try:
            category_instance = Category.objects.get(name=category)
            category_instances.append(category_instance.id)
        except Category.DoesNotExist:
            category_data = {"name": category}
            category_serializer = CategorySerializer(data=category_data)
            category_serializer.is_valid(raise_exception=True)
            category_instance = category_serializer.save()
            category_instances.append(category_instance.id)
    data["categories"] = category_instances

    serializer = ProductSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    product_instance = serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@transaction.atomic
def edit_product(request):
    data = request.data
    product_instance = Product.objects.get(id=data["id"])
    if "add_categories" in data:
        categories = data["add_categories"]
        category_instances = [
            Category.objects.get(name=category).id for category in categories
        ]
        for category in category_instances:
            product_instance.categories.add(category)
        product_instance.save()
        data.pop("add_categories")

    product_serializer = ProductSerializer(instance=product_instance, data=data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()

    return Response(instance=product_instance, data=data)
