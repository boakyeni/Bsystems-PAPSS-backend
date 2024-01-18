# Generated by Django 4.2.7 on 2024-01-18 11:20

from django.db import migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_product_views_productviews"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="categories",
            field=mptt.fields.TreeManyToManyField(
                blank=True, related_name="products", to="inventory.category"
            ),
        ),
    ]
