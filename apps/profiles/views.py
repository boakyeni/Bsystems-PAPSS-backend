from django.shortcuts import render
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Company, Rep, ProfileDocument, ContactPerson
from .serializers import (
    CompanySearchSerializer,
    RepCreateSerializer,
    RepReturnSerializer,
    ProfileDocumentSerializer,
)
from apps.inventory.models import Category
from utils.fuzzysearch import FuzzySearchFilter


# Create your views here.


class SearchForCompany(generics.ListAPIView):
    serializer_class = CompanySearchSerializer
    filter_backends = [
        FuzzySearchFilter,
    ]
    search_fields = ["countries", "company_name"]

    def get_queryset(self):
        category = self.request.query_params.get("category")
        country = self.request.query_params.get("country")
        company_id = self.request.query_params.get("id")
        if category:
            queryset = Company.objects.filter(categories__name__in=[category])
        elif country:
            queryset = Company.objects.filter(countries=country)
        elif company_id:
            company = Company.objects.filter(id=company_id)
            if len(company) > 0:
                queryset = company
            else:
                queryset = []
        else:
            queryset = Company.objects.all()
        return queryset


class SearchForRep(generics.ListAPIView):
    serializer_class = RepReturnSerializer
    filter_backends = [
        filters.SearchFilter,
    ]

    def get_queryset(self):
        queryset = Rep.objects.all()
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

    if not user.contactperson:
        return Response(
            {"error": "Can't do this as a rep"}, status=status.HTTP_204_NO_CONTENT
        )
    serializer = CompanySearchSerializer(
        data=user.contactperson.companies.all(), many=True
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
