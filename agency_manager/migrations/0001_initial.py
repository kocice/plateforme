# Generated by Django 4.1 on 2023-02-02 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Agence",
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
                ("agency_name", models.CharField(max_length=100, unique=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                (
                    "date_create",
                    models.CharField(
                        blank=True,
                        help_text="Pattern = dd-mm-yyyy",
                        max_length=150,
                        null=True,
                    ),
                ),
                (
                    "agency_manager",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Zone",
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
                ("zone_name", models.CharField(max_length=100, unique=True)),
                (
                    "date_create",
                    models.CharField(
                        blank=True,
                        help_text="Pattern = dd-mm-yyyy",
                        max_length=150,
                        null=True,
                    ),
                ),
                (
                    "zone_chief",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Gestionnaire",
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
                    "agence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="agency_manager.agence",
                    ),
                ),
                (
                    "gestionnaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="agence",
            name="zone",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="agency_manager.zone",
            ),
        ),
    ]