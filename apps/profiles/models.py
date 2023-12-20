from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate, now

# Create your models here.
User = get_user_model()


class Country(models.Model):
    # companies = models.ManyToManyField(Company, related_name="Countries", blank=True)
    country = CountryField(
        verbose_name=_("Country"),
        default="GH",
        blank_label="Country",
    )

    def __str__(self):
        return self.country.name


class Company(models.Model):
    company_name = models.CharField(
        max_length=500, verbose_name=_("Company Name"), blank=True, null=True
    )
    address = models.CharField(
        max_length=500, verbose_name=_("Address"), blank=True, null=True
    )
    about = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=250)
    company_phone = PhoneNumberField(blank=True, null=True)
    description = models.TextField(
        verbose_name=_("Company Description"), blank=True, null=True
    )

    verified = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)
    # countries = models.ManyToManyField(Country, blank=True, related_name="companies")
    countries = CountryField(
        verbose_name=_("Country"),
        default="GH",
        blank_label="Country",
    )

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.company_name, filename)

    profile_logo = models.FileField(
        upload_to=user_directory_path, blank=True, null=True
    )

    # def __str__(self):
    #     return str(self.company_name) if self.company_name else ""


class ContactPerson(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="admin_profile",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    phone = PhoneNumberField(max_length=30)
    companies = models.ManyToManyField(
        Company, blank=True, related_name="contact_people"
    )

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.user.id, filename)

    profile_photo = models.FileField(
        upload_to=user_directory_path, blank=True, null=True
    )


class Rep(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "MALE", _("MALE")
        FEMALE = "FEMALE", _("FEMALE")
        NON_BINARY = "NON_BINARY", _("NON_BINARY")

    class TitleChoices(models.TextChoices):
        MR = "Mr", _("Mr")
        MS = "Ms", _("Ms")
        MRS = "Mrs", _("Mrs")
        DEFAULT = "", _("Mr./Ms.")

    class MaritialStatus(models.TextChoices):
        SINGLE = "Single", _("Single")
        MARRIED = "Married", _("Married")
        DIVORCED = "Divorced", _("Divorced")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rep_profile",
    )
    title = models.CharField(
        max_length=50, choices=TitleChoices.choices, default=TitleChoices.DEFAULT
    )
    maritial_status = models.CharField(
        max_length=50,
        choices=MaritialStatus.choices,
        blank=True,
        null=True,
        default=MaritialStatus.choices[0][0],
    )
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"), auto_now_add=True)
    country_of_birth = CountryField(
        verbose_name=_("Country of Birth"), default="GH", blank=False, null=False
    )
    place_of_birth = models.CharField(
        verbose_name=_("Place of Birth"), max_length=250, blank=True, null=True
    )
    first_nationality = models.CharField(
        verbose_name=_("First Nationality"), max_length=250, blank=True, null=True
    )
    second_nationality = models.CharField(
        verbose_name=_("First Nationality"), max_length=250, blank=True, null=True
    )
    address_line_1 = models.CharField(
        verbose_name=_("Address Line 1"), max_length=500, blank=True, null=True
    )
    address_line_2 = models.CharField(
        verbose_name=_("Address Line 2"), max_length=500, blank=True, null=True
    )
    city = models.CharField(max_length=300, blank=True, null=True)
    postal_code = models.CharField(max_length=300, blank=True, null=True)
    region = models.CharField(max_length=300, blank=True, null=True)
    country = CountryField(
        verbose_name=_("Country"),
        default="GH",
        blank_label="Country",
    )
    alternative_email = models.EmailField(blank=True, null=True)
    home_phone = PhoneNumberField(blank=True, null=True, max_length=30)
    mobile_phone = PhoneNumberField(blank=True, null=True, max_length=30)
    work_phone = PhoneNumberField(blank=True, null=True, max_length=30)
    employed = models.BooleanField(blank=True, null=True)
    employer = models.CharField(max_length=500, blank=True, null=True)
    employer_address = models.CharField(max_length=500, blank=True, null=True)
    employer_email = models.EmailField(blank=True, null=True, max_length=250)
    employer_phone = PhoneNumberField(blank=True, null=True, max_length=30)

    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "user_{0}/{1}".format(instance.user.id, filename)

    id_card = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    profile_photo = models.FileField(
        upload_to=user_directory_path, blank=True, null=True
    )


class ProfileDocument(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        filename = instance.name if instance.name else filename
        instance = instance.rep.user.id if instance.rep else instance.uploaded_by.id
        return "user_{0}/{1}".format("main", filename)

    name = models.CharField(
        verbose_name=_("File Name"), blank=True, null=True, max_length=500
    )
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    rep = models.ForeignKey(
        Rep, blank=True, null=True, on_delete=models.CASCADE, related_name="documents"
    )
    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    uploaded_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT, related_name="documents"
    )
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)
