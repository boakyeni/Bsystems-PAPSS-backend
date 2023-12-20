from utils.utils import Base64File
from .models import Rep, Company, ContactPerson, Country, ProfileDocument
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django_countries.serializers import CountryFieldMixin
from phonenumber_field.serializerfields import PhoneNumberField
from django_countries import countries

User = get_user_model()


class CountryFullNameField(serializers.Field):
    def to_representation(self, value):
        # value is the country code
        # Get the full name of the country
        return countries.name(value)

    def to_internal_value(self, data):
        # Convert the full country name to a country code for storage
        for code, name in countries:
            if name.lower() == data.lower():
                return code
        raise serializers.ValidationError("Invalid country name.")


class ProfileDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileDocument
        fields = "__all__"


"""
Serializer is used for both creating a Rep and returning a Rep
"""


class RepCreateSerializer(serializers.ModelSerializer):
    id_card = Base64File(required=False)
    country_of_birth = CountryFullNameField(required=False)
    # country = CountryFullNameField()
    name = serializers.SerializerMethodField()

    profile_photo = Base64File(required=False)

    class Meta:
        model = Rep
        fields = "__all__"

    def get_name(self, obj):
        return obj.user.name if obj.user else ""


class RepReturnSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Rep
        fields = "__all__"

    def get_name(self, obj):
        return obj.user.name if obj.user else ""

    def get_profile_photo(self, obj):
        return (
            "https://www.tradepayafrica.com" + obj.profile_photo.url
            if obj.profile_photo
            else ""
        )


class ContactPersonSerializer(serializers.ModelSerializer):
    profile_photo = Base64File()

    class Meta:
        model = ContactPerson
        fields = "__all__"


class CompanyCreateSerializer(serializers.ModelSerializer):
    profile_logo = Base64File(required=False)

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
    categories = serializers.SerializerMethodField()
    countries = CountryFullNameField()
    profile_logo = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_categories(self, obj):
        return [category.name for category in obj.categories.all()]

    def get_profile_logo(self, obj):
        return (
            "https://www.tradepayafrica.com" + obj.profile_logo.url
            if obj.profile_logo
            else ""
        )


class CountrySerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
