# Generated by Django 4.1 on 2023-03-27 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("credit", "0002_demandecredit_commentaire_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lignecredit",
            name="type_credit",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="credit.typecredit",
            ),
        ),
    ]
