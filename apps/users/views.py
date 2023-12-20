from django.contrib.auth import update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from .serializers import CreateUserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
import random, string
from apps.profiles.serializers import (
    RepCreateSerializer,
    CompanyCreateSerializer,
    ContactPersonSerializer,
    CountrySerializer,
)
from apps.profiles.models import Country
from django.db import transaction
from rest_framework.permissions import AllowAny
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from djoser.serializers import SetPasswordRetypeSerializer
from apps.inventory.serializers import CategorySerializer
from apps.inventory.models import Category


# Create your views here.
class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Send credentials to centralized service
        user = authenticate(request, email=email, password=password)
        if user is not None:
            isFirstLogin = True if password == user.registration_code else False

            token = RefreshToken().for_user(user)
            return Response(
                {
                    "refresh": str(token),
                    "access": str(token.access_token),
                    "isFirstLogin": isFirstLogin,
                }
            )
        else:
            return Response(
                {
                    "errors": "Invalid Credentials",
                    "status": "failed",
                    "message": "Invalid Credentials",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["POST"])
@transaction.atomic
def register(request):
    """
    Check email for prior user then link account to company admin
    """
    data = request.data

    registration_code = "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12
        )
    )
    # Will be changed immediately at first login
    data["password"] = registration_code
    data["registration_code"] = registration_code
    # User Model only stores email to avoid duplicate data in database
    # Refer to Rep or Contact Person
    serializer = CreateUserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data["user"] = user.id

    # Create Rep or Company
    if data["user_type"] == "REP":
        # Create Rep Object
        rep_serializer = RepCreateSerializer(data=data)
        rep_serializer.is_valid(raise_exception=True)
        rep_instance = rep_serializer.save()

    elif data["user_type"] == "COMPANY":
        """Pop Contact person data to avoid conflicts"""
        email_to = data.pop("email")
        data["email"] = data["company_email"]
        contact_data = {}
        contact_data["user"] = user.id
        contact_data["first_name"] = data.pop("first_name")
        contact_data["last_name"] = data.pop("last_name")
        contact_data["email"] = email_to
        contact_data["phone"] = data.pop("contact_phone")
        contact_data["profile_photo"] = data.pop("profile_photo", None)

        # countries = data.pop("countries")
        company_serializer = CompanyCreateSerializer(data=data)
        company_serializer.is_valid(raise_exception=True)
        company_instance = company_serializer.save()

        if "categories" in data:
            for category in data["categories"]:
                category_instance_set = Category.objects.filter(name=category)
                if len(category_instance_set) > 0:
                    category_instance_set[0].companies.add(company_instance)
                    category_instance_set[0].save()

        # for country in countries:
        #     stored_country = Country.objects.filter(country__name=country)
        #     if len(stored_country) > 0:
        #         stored_country[0].companies.add(company_instance)
        #         stored_country[0].save()
        #     else:
        #         country_data = {}
        #         country_data["country"] = country
        #         country_serializer = CountrySerializer(data=country_data)
        #         country_serializer.is_valid(raise_exception=True)
        #         country_instance = country_serializer.save()
        #         country_instance.companies.add(company_instance)

        contact_person_serializer = ContactPersonSerializer(data=contact_data)
        contact_person_serializer.is_valid(raise_exception=True)
        contact_person_instance = contact_person_serializer.save()
        contact_person_instance.companies.add(company_instance)
        contact_person_instance.save()
        company_instance.save()

    context = {"user": user}
    to = [get_user_email(user)]
    if settings.SEND_ACTIVATION_EMAIL:
        settings.EMAIL.activation(request, context).send(to)
    elif settings.SEND_CONFIRMATION_EMAIL:
        settings.EMAIL.confirmation(request, context).send(to)
    return Response(
        {f"Registration Code: {registration_code}"}, status=status.HTTP_201_CREATED
    )


class SetPassword(APIView):
    def post(self, request):
        data = self.request.data
        print(data)
        serializer = SetPasswordRetypeSerializer(
            context={"request": self.request}, data=data
        )
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            logout(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response({"status": 200}, status=status.HTTP_200_OK)
