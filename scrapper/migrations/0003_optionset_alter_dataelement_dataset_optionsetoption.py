# Generated by Django 4.2.7 on 2023-11-30 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scrapper", "0002_remove_dataelement_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OptionSet",
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
                ("dhis_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name="dataelement",
            name="dataset",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="elements",
                to="scrapper.dataset",
            ),
        ),
        migrations.CreateModel(
            name="OptionSetOption",
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
                ("dhis_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "optionset",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="options",
                        to="scrapper.optionset",
                    ),
                ),
            ],
        ),
    ]
