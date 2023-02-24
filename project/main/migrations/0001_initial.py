# Generated by Django 4.1.3 on 2023-02-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AWSCost",
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
                ("user_id", models.CharField(max_length=12)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("usage_type", models.CharField(max_length=255)),
                ("usage_quantity", models.FloatField()),
                ("cost", models.FloatField()),
                ("currency_code", models.CharField(max_length=3)),
                ("exchange_rate", models.FloatField()),
            ],
        ),
    ]
