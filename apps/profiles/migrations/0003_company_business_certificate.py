# Generated by Django 4.2.7 on 2024-01-10 11:07

import apps.profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_company_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="business_certificate",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=apps.profiles.models.Company.user_directory_path,
            ),
        ),
    ]
