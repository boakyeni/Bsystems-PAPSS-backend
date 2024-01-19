# Generated by Django 4.2.7 on 2024-01-19 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_company_business_certificate"),
        ("inventory", "0004_currencyrates_tzs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="seller",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="profiles.company",
            ),
        ),
    ]