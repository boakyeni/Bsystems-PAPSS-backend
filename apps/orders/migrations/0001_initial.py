# Generated by Django 4.2.7 on 2023-12-20 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("inventory", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("INVOICE", "Invoice"),
                            ("DUPLICATE", "Invoice Duplicate"),
                            ("PROFORMA", "Order confirmation"),
                        ],
                        default="PROFORMA",
                        max_length=50,
                    ),
                ),
                ("issued", models.DateField(auto_now_add=True)),
                (
                    "payment_date",
                    models.DateField(blank=True, db_index=True, null=True),
                ),
                (
                    "unit_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "estimated_shipping_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                (
                    "final_shipping_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                (
                    "tax_total",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        blank=True,
                        db_index=True,
                        decimal_places=2,
                        max_digits=4,
                        null=True,
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=7, null=True
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("GHC", "GHC ₵"),
                            ("USD", "USD $"),
                            ("CFA", "CFA"),
                            ("NGN", "NGN ₦"),
                            ("EUR", "EUR €"),
                        ],
                        default="USD",
                        max_length=3,
                    ),
                ),
                (
                    "item_description",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "buyer_name",
                    models.CharField(blank=True, max_length=200, verbose_name="Name"),
                ),
                (
                    "buyer_street",
                    models.CharField(blank=True, max_length=200, verbose_name="Street"),
                ),
                (
                    "buyer_zipcode",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Zip code"
                    ),
                ),
                (
                    "buyer_postal_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "buyer_region",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "buyer_city",
                    models.CharField(blank=True, max_length=200, verbose_name="City"),
                ),
                (
                    "buyer_country",
                    django_countries.fields.CountryField(
                        blank=True, default="PL", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "shipping_name",
                    models.CharField(blank=True, max_length=200, verbose_name="Name"),
                ),
                (
                    "shipping_street",
                    models.CharField(blank=True, max_length=200, verbose_name="Street"),
                ),
                (
                    "shipping_zipcode",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Zip code"
                    ),
                ),
                (
                    "shipping_postal_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "shipping_region",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "shipping_city",
                    models.CharField(blank=True, max_length=200, verbose_name="City"),
                ),
                (
                    "shipping_country",
                    django_countries.fields.CountryField(
                        blank=True, default="PL", max_length=2, verbose_name="Country"
                    ),
                ),
                ("require_shipment", models.BooleanField(db_index=True, default=False)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="buyer",
                    ),
                ),
                (
                    "issuer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                    "order_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="Order Time"),
                ),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "PENDING"),
                            ("PARTIAL", "PARTIAL"),
                            ("FULFILLED", "FULFILLED"),
                            ("CANCELLED", "CANCELLED"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("GHC", "GHC ₵"),
                            ("USD", "USD $"),
                            ("CFA", "CFA"),
                            ("NGN", "NGN ₦"),
                            ("EUR", "EUR €"),
                        ],
                        default="GHC",
                        max_length=50,
                    ),
                ),
                ("note", models.TextField(blank=True, null=True, verbose_name="Note")),
                (
                    "placed_by",
                    models.ForeignKey(
                        max_length=64,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Buyer ID",
                    ),
                ),
                (
                    "placed_to",
                    models.ForeignKey(
                        max_length=64,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.company",
                        verbose_name="Seller ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "transactions_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("key", models.CharField(max_length=512)),
                ("reference", models.CharField(max_length=100)),
                ("amount", models.PositiveIntegerField()),
                ("method", models.CharField(max_length=100)),
                ("status", models.CharField(max_length=100)),
                ("date", models.DateTimeField()),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transactions",
                        to="orders.invoice",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderDetail",
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
                ("quantity", models.IntegerField(default=0)),
                (
                    "subtotal",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=25),
                ),
                (
                    "tax",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "item_code",
                    models.ForeignKey(
                        default=uuid.uuid4,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="orders.order",
                        verbose_name="Order ID",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="invoice",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.order",
                verbose_name="order",
            ),
        ),
    ]
