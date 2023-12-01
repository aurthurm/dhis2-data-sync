# Generated by Django 4.2.7 on 2023-11-27 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scrapper", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataelement",
            name="description",
        ),
        migrations.AlterField(
            model_name="dataelement",
            name="dataset",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="scrapper.dataset",
            ),
        ),
    ]
