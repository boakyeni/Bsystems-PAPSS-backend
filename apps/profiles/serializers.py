from utils.utils import Base64File
from .models import Rep, Company, ContactPerson, Country
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django_countries.serializers import CountryFieldMixin
from phonenumber_field.serializerfields import PhoneNumberField


User = get_user_model()


class RepCreateSerializer(serializers.ModelSerializer):
    id_card = Base64File(required=False)

    class Meta:
        model = Rep
        fields = "__all__"


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = "__all__"


class CompanyCreateSerializer(serializers.ModelSerializer):
    file = Base64File(required=False)

    class Meta:
        model = Company
        fields = "__all__"

    # def create(self, validated_data):
    #     first_name = validated_data.pop("first_name")
    #     last_name = validated_data.pop("last_name")
    #     contact_email = validated_data.pop("contact_email")
    #     phone = validated_data.pop("contact_phone")

    #     User.objects.create()


class CompanySearchSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_category(self, obj):
        return obj.category.name


class CountrySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
