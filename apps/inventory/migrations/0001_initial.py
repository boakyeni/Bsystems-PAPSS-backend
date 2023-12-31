# Generated by Django 4.2.7 on 2023-12-20 12:29

import apps.inventory.models
import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("profiles", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                        help_text="format: required, max-100",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "category_image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.inventory.models.Category.user_directory_path,
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "companies",
                    models.ManyToManyField(
                        blank=True, related_name="categories", to="profiles.company"
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        help_text="format: not required",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="inventory.category",
                        verbose_name="parent of category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="CurrencyRates",
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
                ("currency_rate_timestamp", models.DateTimeField()),
                ("ghs", models.FloatField(blank=True, default=1.0, null=True)),
                ("xof", models.FloatField(blank=True, default=1.0, null=True)),
                ("xaf", models.FloatField(blank=True, default=1.0, null=True)),
                ("ngn", models.FloatField(blank=True, default=1.0, null=True)),
                ("eur", models.FloatField(blank=True, default=1.0, null=True)),
                ("usd", models.FloatField(blank=True, default=1.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductDocument",
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
                        upload_to=apps.inventory.models.ProductDocument.user_directory_path,
                    ),
                ),
                ("date_uploaded", models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                    "image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.inventory.models.ProductImage.user_directory_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                        help_text="format: required, max-255",
                        max_length=255,
                        verbose_name="product name",
                    ),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("sku", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.TextField(
                        help_text="format: required", verbose_name="product description"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="format: true=product visible",
                        verbose_name="product visibility",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="date product last created",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="date product last updated",
                    ),
                ),
                ("weight", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2, default="0.00", max_digits=20
                    ),
                ),
                (
                    "brochure",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.inventory.models.Product.user_directory_path,
                    ),
                ),
                (
                    "categories",
                    mptt.fields.TreeManyToManyField(
                        blank=True, to="inventory.category"
                    ),
                ),
                (
                    "documents",
                    models.ManyToManyField(
                        blank=True,
                        related_name="product",
                        to="inventory.productdocument",
                    ),
                ),
                (
                    "images",
                    models.ManyToManyField(
                        blank=True, related_name="product", to="inventory.productimage"
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.company",
                    ),
                ),
            ],
        ),
    ]
