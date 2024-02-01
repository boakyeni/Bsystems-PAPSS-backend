from django.shortcuts import render
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Company, Rep, ProfileDocument, ContactPerson
from django.db import transaction
from .serializers import (
    CompanySearchSerializer,
    CompanyCreateSerializer,
    RepCreateSerializer,
    RepReturnSerializer,
    ProfileDocumentSerializer,
    CompanyDetailSerializer,
)
from apps.inventory.models import Category
from utils.fuzzysearch import FuzzySearchFilter
from django_countries import countries


# Create your views here.


class SearchForCompany(generics.ListAPIView):
    serializer_class = CompanySearchSerializer
    filter_backends = [
        FuzzySearchFilter,
    ]
    search_fields = ["countries", "company_name"]

    def get_serializer_class(self):
        company_id = self.request.query_params.get("id")
        if company_id:
            return CompanyDetailSerializer  # Use a different serializer for company_id
        return super().get_serializer_class()  # Use the default otherwise

    def get_queryset(self):
        category = self.request.query_params.get("category")
        country = self.request.query_params.get("country")
        company_id = self.request.query_params.get("id")
        if category:
            queryset = Company.objects.filter(
                categories__name__in=[category], is_active=True
            )
        elif country:
            queryset = Company.objects.filter(countries=country, is_active=True)
        elif company_id:
            company = Company.objects.filter(id=company_id)
            if len(company) > 0:
                queryset = company
            else:
                queryset = []
        else:
            queryset = Company.objects.filter(is_active=True)
        return queryset


@api_view(["GET"])
def get_all_countries(request):
    country_codes = set(Company.objects.values_list("countries", flat=True))
    countries_dict = dict(countries)
    country_names_and_codes = [
        {"country": countries_dict[code], "country_code": code}
        for code in country_codes
    ]
    return Response(country_names_and_codes)


@api_view(["PATCH"])
@transaction.atomic
def update_company(request):
    data = request.data
    comp_id = data.get("id", None) or request.query_params.get("id")
    try:
        company_instance = Company.objects.get(id=comp_id)
    except Company.DoesNotExist:
        return Response(
            {
                "error": "No company with this ID",
                "status": "failed",
                "message": "No company Found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Many to Many require manual updating logic
    if "categories" in data:
        for category in data["categories"]:
            category_list = Category.objects.filter(name=category)
            if len(category_list) > 0:
                to_remove = company_instance.categories.first()
                if to_remove:
                    company_instance.categories.remove(to_remove)
                company_instance.categories.add(category_list[0])
    # if "remove_categories" in data:
    #     for category in data["remove_categories"]:
    #         category_list = Category.objects.filter(name=category)
    #         if len(category_list) > 0:
    #             company_instance.categories.remove(category_list[0])
    company_instance.save()
    serializer = CompanyCreateSerializer(
        instance=company_instance, data=data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def disable_company(request):
    # Make only super users capable of this
    company_id = request.query_params.get("id")
    company_instance = Company.objects.filter(id=company_id)
    if len(company_instance):
        company_instance[0].is_active = False
        company_instance[0].save()
    else:
        return Response("No company with that id", status=status.HTTP_400_BAD_REQUEST)
    return Response("company disabled", status=status.HTTP_200_OK)


class SearchForRep(generics.ListAPIView):
    serializer_class = RepReturnSerializer
    filter_backends = [
        filters.SearchFilter,
    ]

    def get_queryset(self):
        queryset = Rep.objects.all()
        rep_id = self.request.query_params.get("id")
        if rep_id:
            queryset = Rep.objects.filter(id=rep_id)
        return queryset


@api_view(["GET"])
def get_number_of_companies(request):
    return Response(
        {"registered_companies": len(Company.objects.all())}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_number_of_reps(request):
    return Response(
        {"registered_reps": len(Rep.objects.all())}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_users_companies(request):
    data = request.data
    user = request.user
    if not user.admin_profile:
        return Response(
            {"error": "Can't do this as a rep"}, status=status.HTTP_204_NO_CONTENT
        )
    serializer = CompanySearchSerializer(
        data=user.admin_profile.companies.all(), many=True
    )
    serializer.is_valid()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_document(request):
    """Currently reps are not associated with a company"""
    data = request.data
    for document in data["documents"]:
        document["uploaded_by"] = request.user.id
        serializer = ProfileDocumentSerializer(data=document)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_document(request):
    data = request.data
    user = request.user

    document_instances = []
    for document in data["documents"]:
        possible_document = ProfileDocument.objects.filter(id=document["documentId"])
        if len(possible_document) > 0:
            document_instance = possible_document[0]
            if user.admin_profile and (
                document_instance.uploaded_by != user
                or (document_instance.company not in user.admin_profile.companies.all())
            ):
                return Response(
                    {
                        "error": f"User is not permitted to delete resource with this name: {document_instance.name}",
                        "message": f"User is not permitted to delete resource with this name: {document_instance.name}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.rep_profile and document_instance.uploaded_by != user:
                return Response(
                    {
                        "error": f"User is not permitted to delete resource with this name: {document_instance.name}",
                        "message": f"User is not permitted to delete resource with this name: {document_instance.name}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            document_instance.delete()
    return Response({"message": "success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def update_company_logo(request):
    """WORK ON LATER"""
    data = request.data
    contact_person = ContactPerson.objects.get(user=request.user.id)
    contact_person.companies.all()


class SearchForDocument(generics.ListAPIView):
    serializer_class = ProfileDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        FuzzySearchFilter,
    ]
    search_fields = ["name", "uploaded_by__name"]

    def get_queryset(self):
        user = self.request.user
        queryset = ProfileDocument.objects.filter(uploaded_by=user)
        return queryset
