from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.SearchProduct.as_view(), name="search-product"),
    path("create-product/", views.create_product, name="create-product"),
    path("total-products/", views.get_number_of_products, name="total"),
]
