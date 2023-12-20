from django.urls import path
from . import views

urlpatterns = [
    path("create-order/", views.create_order, name="create_order"),
    path("edit-order/", views.edit_order, name="edit-order"),
    path("orders/", views.SearchOrder.as_view(), name="search_orders"),
    path("user-orders/", views.SearchUsersOrder.as_view(), name="search_users_orders"),
]
