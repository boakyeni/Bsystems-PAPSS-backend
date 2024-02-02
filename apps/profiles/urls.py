from django.urls import path
from . import views

urlpatterns = [
    path("company/", views.SearchForCompany.as_view(), name="search_for_company"),
    path("total-companies/", views.get_number_of_companies, name="total_companies"),
    path("total-reps/", views.get_number_of_reps, name="total_reps"),
    path("reps/", views.SearchForRep.as_view(), name="search_for_rep"),
    path("my-companies/", views.get_users_companies, name="get_users_companies"),
    path("upload/", views.upload_document, name="upload_document"),
    path("delete-documents/", views.delete_document, name="delete_document"),
    path("edit-company/", views.update_company, name="edit-company"),
    path("get-countries/", views.get_all_countries, name="get_countries"),
    path("disable-company/", views.disable_company),
    path("enable-company/", views.enable_company),
]
