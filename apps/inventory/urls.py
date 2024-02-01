from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.SearchProduct.as_view(), name="search-product"),
    path("create-product/", views.create_product, name="create-product"),
    path("edit-product/", views.edit_product, name="edit_product"),
    path("total-products/", views.get_number_of_products, name="total"),
    path("create-category/", views.CreateCategory.as_view(), name="create_category"),
    path("categories/", views.SearchCategories.as_view(), name="category_search"),
    path("currency-rates/", views.get_currency_rates, name="get_currency_rates"),
    path("edit-category/", views.edit_category, name="update_category"),
    path("disable-product/", views.disable_product),
    path("my-products/", views.get_my_products),
]
