from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("users/set_password/", views.SetPassword.as_view(), name="set_password"),
]
