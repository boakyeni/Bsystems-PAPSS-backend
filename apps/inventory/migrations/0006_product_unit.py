# Generated by Django 4.2.7 on 2024-01-19 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0005_alter_product_seller"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="unit",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]