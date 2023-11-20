from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

# Create your models here.


class User(AbstractUser):
    """ """

    class UserTypes(models.TextChoices):
        COMPANY = "COMPANY", _("Company")
        REP = "REP", _("Rep")

    username = None
    name = models.CharField(verbose_name=_("Name"), max_length=250, default="n/a")
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, blank=True, null=True
    )
    user_type = models.CharField(
        verbose_name=_("User Type"),
        max_length=50,
        choices=UserTypes.choices,
        default="n/a",
    )
    registration_code = models.CharField(max_length=20, default="n/a")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
    ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"

    # @property
    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}"
