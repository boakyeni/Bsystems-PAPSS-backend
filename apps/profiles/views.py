from django.shortcuts import render
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Company, Rep
from .serializers import CompanySearchSerializer

# Create your views here.


class SearchForCompany(generics.ListAPIView):
    serializer_class = CompanySearchSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["country", "company_name"]

    def get_queryset(self):
        category = self.request.query_params.get("category")
        country = self.request.query_params.get("country")
        if category:
            queryset = Company.objects.filter(category__name=category)
        elif country:
            queryset = Company.objects.filter(country=country)
        else:
            queryset = Company.objects.all()
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
