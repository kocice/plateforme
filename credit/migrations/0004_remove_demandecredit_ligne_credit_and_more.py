# Generated by Django 4.1 on 2023-03-27 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("credit", "0003_alter_lignecredit_type_credit"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="demandecredit",
            name="ligne_credit",
        ),
        migrations.AddField(
            model_name="demandecredit",
            name="ligne_credit",
            field=models.ManyToManyField(to="credit.lignecredit"),
        ),
    ]
