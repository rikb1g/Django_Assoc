# Generated by Django 5.1.1 on 2024-11-07 16:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("financeManagment", "0002_categoryfinancemoviment_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financemovements",
            name="file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="financeManager/None/",
                verbose_name="Ficheiro",
            ),
        ),
    ]
