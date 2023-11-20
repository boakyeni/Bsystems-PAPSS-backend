from django.urls import path
from . import views

urlpatterns = [
    path("company/", views.SearchForCompany.as_view(), name="search_for_company"),
    path("total-companies/", views.get_number_of_companies, name="total_companies"),
    path("total-reps/", views.get_number_of_reps, name="total_reps"),
]
