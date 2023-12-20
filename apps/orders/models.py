from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.inventory.models import Product
from apps.profiles.models import Company
import uuid
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from utils.template_email import send_template_email


# Create your models here.
User = get_user_model()


class Order(models.Model):
    """
    Request
    """

    STATUS = (
        ("PENDING", "PENDING"),
        ("PARTIAL", "PARTIAL"),
        ("FULFILLED", "FULFILLED"),
        ("CANCELLED", "CANCELLED"),
    )
    CURRENCY = (
        ("GHC", "GHC ₵"),
        ("USD", "USD $"),
        ("CFA", "CFA"),
        ("NGN", "NGN ₦"),
        ("EUR", "EUR €"),
    )

    placed_by = models.ForeignKey(
        User, verbose_name=_("Buyer ID"), max_length=64, on_delete=models.CASCADE
    )
    placed_to = models.ForeignKey(
        Company, verbose_name=_("Seller ID"), max_length=64, on_delete=models.CASCADE
    )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Time"))
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS[0][0])
    currency = models.CharField(max_length=50, choices=CURRENCY, default=CURRENCY[0][0])
    note = models.TextField(verbose_name=_("Note"), blank=True, null=True)

    def send_order_request_by_email(self):
        mail_context = {
            "user": self.placed_to.company_name,
            "order": self.id,
            "order_object": self,
            "buyer": self.placed_by,
        }
        send_template_email(
            [self.placed_to.email],
            "mail/order_created_title.txt",
            "mail/order_created_body.html",
            mail_context,
            None,
        )


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="details",
        on_delete=models.CASCADE,
        verbose_name=_("Order ID"),
        default=0,
    )
    item_code = models.ForeignKey(Product, on_delete=models.CASCADE, default=uuid.uuid4)
    quantity = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def product_name(self):
        return self.item_code.name

    # @property
    # def unit_price(self):
    #     return self.item_code.price


class Invoice(models.Model):
    INVOICE_TYPES = (
        ("INVOICE", _("Invoice")),
        ("DUPLICATE", _("Invoice Duplicate")),
        ("PROFORMA", _("Order confirmation")),
    )
    CURRENCY = (
        ("GHC", "GHC ₵"),
        ("USD", "USD $"),
        ("CFA", "CFA"),
        ("NGN", "NGN ₦"),
        ("EUR", "EUR €"),
    )
    type = models.CharField(
        max_length=50, choices=INVOICE_TYPES, default=INVOICE_TYPES[2][0]
    )
    buyer = models.ForeignKey(User, verbose_name=_("buyer"), on_delete=models.CASCADE)
    issuer = models.ForeignKey(Company, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE)
    issued = models.DateField(auto_now_add=True)
    payment_date = models.DateField(db_index=True, blank=True, null=True)
    unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    quantity = models.IntegerField(default=1)
    estimated_shipping_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    final_shipping_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    tax_total = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    tax = models.DecimalField(
        max_digits=4, decimal_places=2, db_index=True, null=True, blank=True
    )  # Tax=None is whet tax is not applicable
    total = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY, default=CURRENCY[1][0])
    item_description = models.CharField(max_length=200, blank=True, null=True)
    buyer_name = models.CharField(max_length=200, verbose_name=_("Name"), blank=True)
    buyer_street = models.CharField(
        max_length=200, verbose_name=_("Street"), blank=True
    )
    buyer_zipcode = models.CharField(
        max_length=200, verbose_name=_("Zip code"), blank=True
    )
    buyer_postal_code = models.CharField(max_length=100, blank=True, null=True)
    buyer_region = models.CharField(max_length=300, blank=True, null=True)
    buyer_city = models.CharField(max_length=200, verbose_name=_("City"), blank=True)
    buyer_country = CountryField(verbose_name=_("Country"), default="PL", blank=True)
    shipping_name = models.CharField(max_length=200, verbose_name=_("Name"), blank=True)
    shipping_street = models.CharField(
        max_length=200, verbose_name=_("Street"), blank=True
    )
    shipping_zipcode = models.CharField(
        max_length=200, verbose_name=_("Zip code"), blank=True
    )
    shipping_postal_code = models.CharField(max_length=100, blank=True, null=True)
    shipping_region = models.CharField(max_length=250, blank=True, null=True)
    shipping_city = models.CharField(max_length=200, verbose_name=_("City"), blank=True)
    shipping_country = CountryField(verbose_name=_("Country"), default="PL", blank=True)
    require_shipment = models.BooleanField(default=False, db_index=True)

    def send_invoice_by_email(self):
        mail_context = {
            "user": self.buyer,
            "invoice_type": self.type,
            "invoice_number": self.id,
            "order": self.order.id,
            "order_object": self.order,
        }
        send_template_email(
            [self.buyer.email],
            "mail/invoice_created_title.txt",
            "mail/invoice_created_body.html",
            mail_context,
            None,
        )


class Transaction(models.Model):
    transactions_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice,
        related_name="transactions",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    key = models.CharField(max_length=512)
    reference = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.transactions_id) if self.transactions_id else ""
