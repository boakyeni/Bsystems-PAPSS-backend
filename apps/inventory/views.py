from django.shortcuts import render
from rest_framework import generics, filters, status, permissions
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    ProductReturnSerializer,
    ProductCreateSerializer,
    CategorySerializer,
    ProductImageSerializer,
    CurrencyRatesSerializer,
    ProductDocumentSerializer,
    CategoryReturnSerializer,
)
from .models import Product, Category, CurrencyRates, Company
from rest_framework.response import Response
from django.db import transaction
from rest_framework.views import APIView
from django.utils.timezone import now
from datetime import timedelta

# Create your views here.

from utils.fuzzysearch import FuzzySearchFilter


class SearchProduct(generics.ListAPIView):
    """
    Fuzzy Search allows for typos, but the tradeoff is speed,
    increasing fuzz ratio in utils.fuzzysearch will yield faster results,
    and decreasing will yield slower results but allows for greater margin
    or error when searching
    """

    serializer_class = ProductReturnSerializer
    filter_backends = [
        FuzzySearchFilter,
    ]
    search_fields = ["name", "description"]

    def get_queryset(self):
        queryset = Product.objects.all()
        product_id = self.request.query_params.get("id")
        if product_id:
            product = Product.objects.filter(id=product_id)
            if len(product) > 0:
                queryset = product
            else:
                queryset = []
        return queryset


@api_view(["GET"])
def get_number_of_products(request):
    return Response(
        {"uploaded_products": len(Product.objects.all())}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def create_product(request):
    data = request.data

    # temporariliy here for dev or maybe not? If a contact person has many companies then they
    # need to explicitly state which company to add this product to
    seller_name = data["seller"]
    company_query = Company.objects.filter(company_name=seller_name)
    if len(company_query) == 1:
        company_instance = company_query[0]
        data["seller"] = company_instance.id
    else:
        # For dev this is fine, in prod this should throw an Error that the company
        # does not exist
        data.pop("seller")

    categories = []

    if "categories" in data:
        categories = data["categories"]
    category_instances = []
    # requiring a product to have categories, better error handling should be here
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

    image_instances = []
    if "images" in data:
        images = data["images"]
        for image in images:
            image_data = {"image": image}
            image_serializer = ProductImageSerializer(data=image_data)
            image_serializer.is_valid(raise_exception=True)
            image_instance = image_serializer.save()
            image_instances.append(image_instance.id)
    data["images"] = image_instances

    document_instances = []
    if "documents" in data:
        documents = data["documents"]
        for document in documents:
            document_serializer = ProductDocumentSerializer(data=document)
            document_serializer.is_valid(raise_exception=True)
            document_instance = document_serializer.save()
            document_instances.append(document_instance.id)
    data["documents"] = document_instances

    serializer = ProductCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    product_instance = serializer.save()

    return_serializer = ProductReturnSerializer(instance=product_instance)

    return Response(return_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@transaction.atomic
def edit_product(request):
    data = request.data
    product_instance = Product.objects.get(id=data["id"])
    # Category must already be in the database
    if "add_categories" in data:
        categories = data["add_categories"]
        category_instances = [
            Category.objects.get(name=category).id for category in categories
        ]
        for category in category_instances:
            product_instance.categories.add(category)
        product_instance.save()
        # add_categories is not a field in Product so best to remove it from data to be sent to Product
        data.pop("add_categories")
    # Product Document is many to many to Product, so serilize and then add to Product
    if "add_documents" in data:
        documents = data["add_documents"]
        for document in documents:
            document_serializer = ProductDocumentSerializer(data=document)
            document_serializer.is_valid(raise_exception=True)
            document_instance = document_serializer.save()
            product_instance.documents.add(document_instance.id)
        product_instance.save()
        # add_documents is not a field in Product so best to remove it from data to be sent to Product
        data.pop("add_documents")
    if "delete_documents" in data:
        # documents are not actually deleted, but set to inactive, users should then
        # have the option to grab from trash within a period of time
        documents = data["delete_documents"]

    product_serializer = ProductReturnSerializer(instance=product_instance, data=data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()

    return Response(product_serializer.data, status=status.HTTP_200_OK)


class SearchCategories(generics.ListAPIView):
    serializer_class = CategoryReturnSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class CreateCategory(APIView):
    @transaction.atomic
    def post(self, request):
        data = request.data
        if "parent" in data:
            try:
                parent_instance = Category.objects.get(name=data["parent"])
                data.pop("parent")
                serializer = CategorySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                category = serializer.save()
                category.parent = parent_instance
                category.save()
            except Category.DoesNotExist:
                custom_response_data = {
                    # customize your response format here
                    "errors": "Category not found",
                    "status": "failed",
                    "message": "Category of the name requested as parent category does not exist",
                }
                return Response(
                    custom_response_data, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = CategorySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            category = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@transaction.atomic
def get_currency_rates(request):
    rates = None
    data = request.data
    try:
        rates = CurrencyRates.objects.get()
    except CurrencyRates.DoesNotExist:
        data["currency_rate_timestamp"] = now() - timedelta(hours=3)
        serializer = CurrencyRatesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        rates = serializer.save()

    serializer = CurrencyRatesSerializer(rates)
    return Response(serializer.data, status=status.HTTP_200_OK)
