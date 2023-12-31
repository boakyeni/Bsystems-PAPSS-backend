# Generated by Django 4.2.7 on 2023-12-20 12:29

import apps.profiles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Company Name",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=500, null=True, verbose_name="Address"
                    ),
                ),
                ("about", models.TextField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=250, null=True)),
                (
                    "company_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Company Description"
                    ),
                ),
                ("verified", models.BooleanField(default=False)),
                ("registration_date", models.DateField(auto_now_add=True)),
                (
                    "countries",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "profile_logo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.Company.user_directory_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Ms", "Ms"),
                            ("Mrs", "Mrs"),
                            ("", "Mr./Ms."),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
                (
                    "maritial_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Single", "Single"),
                            ("Married", "Married"),
                            ("Divorced", "Divorced"),
                        ],
                        default="Single",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(auto_now_add=True, verbose_name="Date of Birth"),
                ),
                (
                    "country_of_birth",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country of Birth"
                    ),
                ),
                (
                    "place_of_birth",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Place of Birth",
                    ),
                ),
                (
                    "first_nationality",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="First Nationality",
                    ),
                ),
                (
                    "second_nationality",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="First Nationality",
                    ),
                ),
                (
                    "address_line_1",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Address Line 1",
                    ),
                ),
                (
                    "address_line_2",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Address Line 2",
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "postal_code",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("region", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="GH", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "alternative_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "home_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=30, null=True, region=None
                    ),
                ),
                (
                    "mobile_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=30, null=True, region=None
                    ),
                ),
                (
                    "work_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=30, null=True, region=None
                    ),
                ),
                ("employed", models.BooleanField(blank=True, null=True)),
                ("employer", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "employer_address",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "employer_email",
                    models.EmailField(blank=True, max_length=250, null=True),
                ),
                (
                    "employer_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=30, null=True, region=None
                    ),
                ),
                (
                    "id_card",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.Rep.user_directory_path,
                    ),
                ),
                (
                    "profile_photo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.Rep.user_directory_path,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rep_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfileDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=500, null=True, verbose_name="File Name"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.ProfileDocument.user_directory_path,
                    ),
                ),
                ("date_uploaded", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="profiles.company",
                    ),
                ),
                (
                    "rep",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="profiles.rep",
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContactPerson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=250)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=30, region=None
                    ),
                ),
                (
                    "profile_photo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.ContactPerson.user_directory_path,
                    ),
                ),
                (
                    "companies",
                    models.ManyToManyField(
                        blank=True, related_name="contact_people", to="profiles.company"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
