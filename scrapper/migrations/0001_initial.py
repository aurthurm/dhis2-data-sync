# Generated by Django 4.2.7 on 2023-11-27 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DataElement",
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
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="DataSet",
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
        migrations.CreateModel(
            name="OrganisatinalUnit",
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
        migrations.CreateModel(
            name="DataImport",
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
                ("period", models.CharField(blank=True, max_length=20)),
                ("value", models.CharField(blank=True, max_length=255)),
                ("comment", models.TextField(blank=True)),
                ("followup", models.CharField(blank=True, max_length=255)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "dataelement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="scrapper.dataelement",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="scrapper.dataset",
                    ),
                ),
                (
                    "ornanisationunit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="scrapper.organisatinalunit",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="dataelement",
            name="dataset",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="scrapper.dataset"
            ),
        ),
    ]
